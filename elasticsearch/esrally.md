- [Elasticsearch 压测方案之 esrally 简介](https://segmentfault.com/a/1190000011174694)

```bash
esrally --track-path=/data/secoo_program/esrally/tutorial/ --pipeline=benchmark-only --target-hosts=192.168.41.4:9200,192.168.41.5:9200,192.168.41.6:9200,192.168.41.7:9200,192.168.41.8:9200,192.168.41.9:9200 --client-options="use_ssl:false,verify_certs:true,basic_auth_user:'elastic',basic_auth_password:'fcj5cU1Oh3YUcU3NL6vw'" --offline --report-file=/tmp/logs/report.md



esrally race --pipeline=benchmark-only --target-hosts=127.0.0.1:9200 --cluster-health=yellow --track=nyc_taxis --challenge=append-no-conflicts


-- 本地环境的用户权限不足
esrally race --pipeline=benchmark-only --target-hosts=es-test-ag.umlife.net:80 --track=nyc_taxis --challenge=append-no-conflicts --test-mode --client-options="use_ssl:false,verify_certs:false,basic_auth_user:'ag_adm',basic_auth_password:'xxx'"  --report-file=/tmp/logs/report.md


esrally race --pipeline=benchmark-only --target-hosts=127.0.0.1:9200 --track=nyc_taxis --challenge=append-no-conflicts --test-mode --user-tag=[version:info]
```
> 通过修改logging的等级，进行ES的请求日志查看。



-----
# TODO

- [ElasticSearch 集群压力测试指南](https://mp.weixin.qq.com/s/kzEazBDlphFxfxJmVBQhYA)

如何做压测？

测试的指标？

测试的数据？

测试的流程？

测试的结果对比？


