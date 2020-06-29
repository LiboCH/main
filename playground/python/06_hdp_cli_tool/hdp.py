import requests
import logging
import sys
import json
import time

u='admin'
p='admin'
h='h1:8080'
#logging.basicConfig(stream=sys.stdout,level=logging.DEBUG,format='%(asctime)s| %(levelname)s | %(name)s | %(message)s')
logging.basicConfig(stream=sys.stdout,format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
            datefmt='%Y-%m-%d:%H:%M:%S',
                level=logging.DEBUG)
#jlogging.basicConfig(filename='log',level=logging.DEBUG,format='%(asctime)s| %(levelname)s | %(name)s | %(message)s')
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
        logging.debug(f'In self.get, req: {req}')
        resp = requests.get(req, auth=(self._ambari_user,self._ambari_password))
        if resp:
            return resp
        else:
            logging.error(f'Get request unsuccessful. Message: {resp.text}')

    def put(self,url,data):
        headers={'X-Requested-By': 'ambari'}
        req = self._url+self.cluster_name+'/'+url
        logging.debug(f'In self.put, req: {req} data: {data}')
        resp=requests.put(req, data=data, headers=headers, auth=(self._ambari_user,self._ambari_password))
        if resp:
            return resp
        else:
            logging.error(f'Get request unsuccessful. Message: {resp.text}')



    def _check_protocol(self):
        # to determine if HTTP or HTTPS
        try:
            url="https://"+self._ambari_host+"/api/v1/clusters/"
            logging.debug("Trying HTTPS connection to: "+url)
            resp = requests.get(url,auth=(self._ambari_user,self._ambari_password))
            resp.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            logging.error(http_err)
        except Exception as err:
            url="http://"+self._ambari_host+"/api/v1/clusters/"
            logging.warning("HTTPS connection failed, trying HTTP: " +url)
            try:
                resp = requests.get(url,auth=(self._ambari_user,self._ambari_password))
                resp.raise_for_status()
            except requests.exceptions.HTTPError as http_err:
                logging.error(http_err)
            except Exception as err:
                logging.error(err)
            else:
                return url
        else:
            return url

    def _get_cluster_name(self):
        resp = requests.get(self._url,auth=(self._ambari_user,self._ambari_password))
        cluster_name=resp.json()['items'][0]['Clusters']['cluster_name']
        logging.info('Discovered cluster name: '+cluster_name)
        return cluster_name

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
        logging.error(f'Command: {command} not in list of allowed commands') if command not in _command_dic else None
        if self.check_service_status(service) != _command_dic[command]['ambari_desired_state']:
            logging.info(_command_dic[command]['context_message'])
            data={}
            data['RequestInfo']={}
            data['RequestInfo']['context']=_command_dic[command]['context_message']
            data['Body']={}
            data['Body']['ServiceInfo']={'state':_command_dic[command]['ambari_desired_state']}
            logging.debug(f'Start service data: {data}')
            self.put("services/"+service,json.dumps(data))
            service_status='UNKNOWN'
            command_timeout=20
            while service_status != _command_dic[command]['ambari_desired_state'] and command_timeout > 0:
                time.sleep(3)
                command_timeout-=1
                service_status=self.check_service_status(service)
                logging.debug(self.check_service_status(service))

        else:
            logging.warning(f'Service: {service} already in requested state: '+ _command_dic[command]['ambari_desired_state'])


    def check_service_exists(self,service):
        resp = self.get('services/'+service)
        logging.debug(f'Service: {service} exists: '+ ('True' if resp else 'False'))
        return True if resp.status_code == 200 else False

    def start_service(self,service):
        if self.check_service_status(service) != 'STARTED':
            logging.info(f'Starting service: {service}')
            data_string= '{"RequestInfo": {"context" :"Start HDFS via REST"}, "Body": {"ServiceInfo": {"state": "STARTED"}}}'
            data={}
            data['RequestInfo']={}
            data['RequestInfo']['context']=f'Start {service} via REST';
            data['Body']={}
            data['Body']['ServiceInfo']={'state':'STARTED'}
            logging.debug(f'Start service data: {data}')
            #self.put("services/"+service,json.dumps(data))
            self.put("services/"+service,data_string)
            service_status='UNKNOWN'
            while service_status != 'STARTED':
                time.sleep(3)
                logging.debug(self.check_service_status(service))
                service_status=self.check_service_status(service)

        else:
            logging.warning(f'Service: {service} already in state: STARTED')


    def stop_service(self,service):
        if self.check_service_status(service) != 'INSTALLED':
            logging.info(f'Stopping service: {service}')
            data_string= '{"RequestInfo": {"context" :"Stop HDFS via REST"}, "Body": {"ServiceInfo": {"state": "INSTALLED"}}}'
            data={}
            data['RequestInfo']={}
            data['RequestInfo']['context']=f'Start {service} via REST';
            data['Body']={}
            data['Body']['ServiceInfo']={'state':'INSTALLED'}
            logging.debug(f'Stop service data: {data}')
            self.put("services/"+service,json.dumps(data))
            #self.put("services/"+service,data_string)
        else:
            logging.warning(f'Service: {service} already in state: INSTALLED')

        pass

    def check_service_status(self, service):
        if self.check_service_exists(service):
            service_status = self.get('services/'+service).json()['ServiceInfo']['state']
            logging.debug(f'In check_service_status, status:{service_status}')
            return self.get('services/'+service).json()['ServiceInfo']['state']
        else:
            logging.error(f'Service: {service} does not exists')

    def __str__(self):
        return f'Cluster name: {self.cluster_name}\nAmbari url: {self._url}'

if __name__ == '__main__' :
    my_cluster = HDPCluster(h,u,p)
    #print(my_cluster.start_service('HDFS'))
    print(my_cluster.stop_service('HDFS'))
