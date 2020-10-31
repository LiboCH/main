docker run \
    -p 9090:9090 \
    -v /home/libo/git/liboch/main/playground/docker/08_prometheus/prometheus.yml:/etc/prometheus/prometheus.yml \
    prom/prometheus
