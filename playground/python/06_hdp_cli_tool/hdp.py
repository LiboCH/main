import requests
import logging
import sys
import json
import time
from lib.progresbar import monMaster

u='admin'
p='admin'
h='h1:8080'
#logging.basicConfig(stream=sys.stdout,format='%(asctime)s,%(msecs)-3d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
#            datefmt='%Y-%m-%d:%H:%M:%S',
#                level=logging.WARNING)
logging.basicConfig(filename='log',format='%(asctime)s,%(msecs)-3d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
            datefmt='%Y-%m-%d:%H:%M:%S',
                level=logging.WARNING)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
#hdp cluster status
#hdp cluster start
#hdp cluster stop
#hdp sr delete --no-backup
#hdp kafka delete  

#1 check http/https
#2 get clustter name

class HDPCluster:
    def __init__(self,ambari_host, ambari_user, ambari_password):
        self._ambari_host=ambari_host
        self._ambari_user=ambari_user
        self._ambari_password=ambari_password
        self._url=self._check_protocol()
        self.cluster_name=self._get_cluster_name()
    
    def get(self,url):
        req = self._url+self.cluster_name+'/'+url
        logger.debug(f'In self.get, req: {req}')
        resp = requests.get(req, auth=(self._ambari_user,self._ambari_password))
        if resp:
            return resp
        else:
            logger.error(f'Get request unsuccessful. Message: {resp.text}')

    def put(self,url,data):
        headers={'X-Requested-By': 'ambari'}
        req = self._url+self.cluster_name+'/'+url
        logger.debug(f'In self.put, req: {req} data: {data}')
        resp=requests.put(req, data=data, headers=headers, auth=(self._ambari_user,self._ambari_password))
        if resp:
            return resp
        else:
            logger.error(f'Get request unsuccessful. Message: {resp.text}')



    def _check_protocol(self):
        # to determine if HTTP or HTTPS
        try:
            url="https://"+self._ambari_host+"/api/v1/clusters/"
            logger.debug("Trying HTTPS connection to: "+url)
            resp = requests.get(url,auth=(self._ambari_user,self._ambari_password))
            resp.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            logger.error(http_err)
        except Exception as err:
            url="http://"+self._ambari_host+"/api/v1/clusters/"
            logger.warning("HTTPS connection failed, trying HTTP: " +url)
            try:
                resp = requests.get(url,auth=(self._ambari_user,self._ambari_password))
                resp.raise_for_status()
            except requests.exceptions.HTTPError as http_err:
                logger.error(http_err)
            except Exception as err:
                logger.error(err)
            else:
                return url
        else:
            return url

    def _get_cluster_name(self):
        resp = requests.get(self._url,auth=(self._ambari_user,self._ambari_password))
        cluster_name=resp.json()['items'][0]['Clusters']['cluster_name']
        logger.info('Discovered cluster name: '+cluster_name)
        return cluster_name
    
    def _get_component_state(self,service,component):
        resp = self.get('services/'+service+'/components/'+component).json()
        _component_counters=''
        for key,value in resp['ServiceComponentInfo'].items():
            if "count" in key or key == "state":
                _component_counters=_component_counters+key+":"+str(value)+"\n"

        logger.debug(f'List of counters for service:{service},  component: {component}\n{_component_counters}')
        ##status logic
        if resp['ServiceComponentInfo']['total_count'] == 0 : return 'INACTIVE'
        if resp['ServiceComponentInfo']['state'] == 'INSTALLED':
            if resp['ServiceComponentInfo']['total_count'] == resp['ServiceComponentInfo']['installed_count'] : return 'STOPPED'
            if resp['ServiceComponentInfo']['total_count'] > resp['ServiceComponentInfo']['installed_count'] : return 'STOPPING'
        if resp['ServiceComponentInfo']['state'] == 'STARTED':
            if resp['ServiceComponentInfo']['total_count'] == resp['ServiceComponentInfo']['started_count'] : return 'STARTED'
            if resp['ServiceComponentInfo']['total_count'] == resp['ServiceComponentInfo']['started_count'] + resp['ServiceComponentInfo']['installed_count'] - resp['ServiceComponentInfo']['installed_and_maintenance_off_count']: return 'MAITENENCE'
            if resp['ServiceComponentInfo']['total_count'] > resp['ServiceComponentInfo']['started_count'] + resp['ServiceComponentInfo']['installed_count'] - resp['ServiceComponentInfo']['installed_and_maintenance_off_count'] : return 'STARTING'



    def _get_service_active_components(self,service):
        resp = self.get('services/'+service+'/components').json()
        _component_list = "\n".join(item['ServiceComponentInfo']['component_name'] for item in resp['items'])
        logger.debug(f'List of ALL components for service: {service}\n{_component_list}')
        #checking for active components 
        for item in resp['items']:
            logger.info(f'Detected state for service:'+ item['ServiceComponentInfo']['service_name'] + ' componnent: '+ item['ServiceComponentInfo']['component_name'] +' -> '+ self._get_component_state(item['ServiceComponentInfo']['service_name'], item['ServiceComponentInfo']['component_name']))

    def _send_service_command(self,service,command):
        _command_dic={'start':
                            {   'ambari_desired_state':'STARTED',
                                'context_message':'Starting ' + service +' via REST'
                             },
                       'stop':
                            {   'ambari_desired_state':'INSTALLED',
                                'context_message':'Stopping ' + service +' via REST'
                             }
                      }
        logger.error(f'Command: {command} not in list of allowed commands') if command not in _command_dic else None

        service_status=self.check_service_status(service)
        if  service_status != _command_dic[command]['ambari_desired_state']:
            logger.info(_command_dic[command]['context_message'])
            data={}
            data['RequestInfo']={}
            data['RequestInfo']['context']=_command_dic[command]['context_message']
            data['Body']={}
            data['Body']['ServiceInfo']={'state':_command_dic[command]['ambari_desired_state']}
            logger.debug(f'Start service data: {data}')
            self.put("services/"+service,json.dumps(data))
            command_timeout=60
            while service_status != _command_dic[command]['ambari_desired_state'] and command_timeout > 0:
                command_timeout-=1
                self._get_service_active_components(service)
                logger.info('Current service status: '+self.check_service_status(service) + ', requested opperation in progress... Timeout in '+ str(command_timeout*3) + 's')
                time.sleep(3)
                service_status=self.check_service_status(service)
            if command_timeout <= 0 :
                logger.error(f"Time for operation: {command} on service: {service} reached... Please check Ambari for status")
            logger.info(f'Service: {service} -> {service_status}')

        else:
            logger.warning(f'Service: {service} already in requested state: '+ _command_dic[command]['ambari_desired_state'])


    def check_service_exists(self,service):
        resp = self.get('services/'+service)
        logger.debug(f'Service: {service} exists: '+ ('True' if resp else 'False'))
        return True if resp.status_code == 200 else False

    def start_service(self,service):
        self._send_service_command(service,'start')

    def stop_service(self,service):
        self._send_service_command(service,'stop')

    def check_service_status(self, service):
        if self.check_service_exists(service):
            service_status = self.get('services/'+service).json()['ServiceInfo']['state']
            logger.debug(f'In check_service_status, status:{service_status}')
            return self.get('services/'+service).json()['ServiceInfo']['state']
        else:
            logger.error(f'Service: {service} does not exists')

    def __str__(self):
        return f'Cluster name: {self.cluster_name}\nAmbari url: {self._url}'

if __name__ == '__main__' :
    my_cluster = HDPCluster(h,u,p)
    monitor=monMaster('/some/log/path');
    monitor.start('Stopping HBASE')
    my_cluster.stop_service('HBASE')
    monitor.stop('Stopping HBASE','success')
    #my_cluster.stop_service('HBASE')
    #print(my_cluster._get_service_active_components('HDFS'))
