# kafka的基本命令


```bash
ssh -p36000 kafka-00.ag.awsor
cd /opt/kafka_2.13-2.6.0


# 创建主题
bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 0 --partitions 2 --topic addata.ad_heat

# 主题信息
bin/kafka-topics.sh --describe --zookeeper 192.168.1.100:2181 --topic addata.ad_heat

# 命令行生产者
./bin/kafka-console-producer.sh --broker-list localhost:9092 --topic addata.ad_heat

# 消费者
./bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic mykafka --from-beginning

# 获取主题情况
bin/kafka-topics.sh --zookeeper 172.16.8.4:2181 --list

# 获取消费者消费情况
bin/kafka-consumer-groups.sh --describe --bootstrap-server localhost:9092 --group common

# 更改topic的配置
kafka-topics.sh --zookeeper 172.16.8.4:2181 --alter --topic <topic name> --config retention.ms=1000

# 获取topic的配置
kafka-configs --zookeeper 172.16.8.4:2181 --entity-type topics --describe --entity-name web_log

# e.g.:
kafka-consumer-groups.sh --bootstrap-server <kafka_broker_host:9091> --group <group_name> --reset-offsets --to-offset 1000 --topic <my-topic> --execute


--topic t1:0,1,2（为指定的topic分区调整位移）

--to-earliest
--to-latest
--to-offset 100
--shift-by -10

bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group common --reset-offsets --to-offset 100 --topic addata.ad_heat --execute


./bin/kafka-topics.sh --describe --zookeeper zk-00.ag.alishh:2181/kafka/ag --topic binlog-db40-adData-ad-heat

./bin/kafka-consumer-groups.sh --describe --bootstrap-server kafka-00.ag.alishh:9092 --group common

./bin/kafka-consumer-groups.sh --bootstrap-server kafka-00.ag.alishh:9092 --group common --reset-offsets --shift-by -10 --topic binlog-db40-adData-ad-heat:0 --execute

```


----
# production

ssh -p36000 kafka-00.ag.alishh


# 海外
ssh -p36000 kafka-00.ag.awsor


## 热度
~/bin/kafka/bin/kafka-consumer-groups.sh --describe --bootstrap-server kafka-00.ag.awsor:9092 --group ag_web_heat

~/bin/kafka/bin/kafka-consumer-groups.sh --bootstrap-server kafka-00.ag.awsor:9092 --group ag_web_heat --reset-offsets --shift-by -10 --topic binlog_db_10_adData_ad_heat:0 --execute

./kafka/bin/kafka-consumer-groups.sh --bootstrap-server kafka-00.ag.awsor:9092 --group ag_web_heat --reset-offsets --to-latest --all-topics --execute


----
# 本地

cd opt/kafka

./bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group common --reset-offsets --to-latest --all-topics --execute

./bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group common --reset-offsets --shift-by -1 --topic addata.ad_heat:0 --execute

./bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic bin_qs

./bin/kafka-consumer-groups.sh --describe --bootstrap-server localhost:9092 --group common


## 命令行消费信息

./bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic addata.ad_heat --from-beginning

./bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic addata.ad_heat  --max-messages 1

./bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic addata.ad_heat --offset latest --partition 0

./bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic addata.ad_heat --offset latest --partition 0 --max-messages 1


----

# 国内
```bash

ssh -p36000 kafka-00.ag.alishh
ssh -p36000 kafka-00.mh.alishh

cd bin/kafka

zk-00.ag.alishh:2181

zk-00.ag.alishh:2181/kafka/mh

kafka-00.mh.alishh:9092

kafka-00.ag.alishh:9092

## 主题信息
bin/kafka-topics.sh --describe --zookeeper zk-00.ag.alishh:2181/kafka/ag --topic binlog-pub-db-00-msp-org-brand
bin/kafka-topics.sh --describe --zookeeper zk-00.ag.alishh:2181/kafka/mh --topic binlog-mh-db-33-mh-douyin-measure-douyin-video-measure

## 重置
./bin/kafka-consumer-groups.sh --bootstrap-server kafka-00.ag.alishh:9092 --group ag_ec_sync_product_qs --reset-offsets --to-latest --all-topics --execute

## 描述
./bin/kafka-consumer-groups.sh --describe --bootstrap-server kafka-00.ag.alishh:9092 --group dj-ch-sync-river
./bin/kafka-consumer-groups.sh --describe --bootstrap-server kafka-00.ag.alishh:9092 --group es_sync_campaign_record
./bin/kafka-consumer-groups.sh --describe --bootstrap-server kafka-00.mh.alishh:9092 --group es_sync_campaign_record

## 消费消息
./bin/kafka-console-consumer.sh --bootstrap-server kafka-00.ag.alishh:9092 --topic binlog-db10-ecData-product-qs-growth --from-beginning

### 消费最多10个消息
./bin/kafka-console-consumer.sh --bootstrap-server kafka-00.ag.alishh:9092 --topic binlog-db10-ecData-product-qs-growth --max-messages 0

./bin/kafka-console-consumer.sh --bootstrap-server kafka-00.ag.alishh:9092 --topic binlog-ag-db-11-ecdata-v3-ad-category-relation --max-messages 1  --consumer-property group.id=dj-ch-sync-river

./bin/kafka-console-consumer.sh --bootstrap-server kafka-00.mh.alishh:9092 --topic binlog-mh-db-33-mh-douyin-measure-douyin-video-measure --max-messages 10  --consumer-property group.id=dj-ch-sync-river

# 删除消费组
./bin/kafka-consumer-groups.sh --bootstrap-server kafka-00.ag.alishh:9092 --group es_sync_ad_ec_product_area --delete
./bin/kafka-consumer-groups.sh --bootstrap-server kafka-00.mh.alishh:9092  --delete-offsets --group dj-ch-sync-river --topic binlog-mh-db-33-mh-douyin-measure-douyin-video-measure

## 偏移
./bin/kafka-consumer-groups.sh --bootstrap-server kafka-00.ag.alishh:9092 --group dj-ch-sync-river --reset-offsets --shift-by -10 --topic binlog-ag-db-11-ecdata-v3-ad-category-relation:0 --execute

./bin/kafka-consumer-groups.sh --bootstrap-server kafka-00.ag.alishh:9092 --group test_ag_web_uni --reset-offsets --shift-by -10 --topic binlog-db40-adData-ad-heat:0 --execute

./bin/kafka-consumer-groups.sh --bootstrap-server kafka-00.mh.alishh:9092 --group dj-ch-sync-river --reset-offsets --shift-by -100 --topic binlog-mh-db-33-mh-douyin-measure-douyin-video-measure:0 --execute

./bin/kafka-consumer-groups.sh --bootstrap-server kafka-00.mh.alishh:9092 --group dj-ch-sync-river --reset-offsets --to-latest --topic binlog-mh-db-33-mh-douyin-measure-douyin-video-measure --execute

./bin/kafka-consumer-groups.sh --bootstrap-server kafka-00.ag.alishh:9092 --group test_ag_web_uni --reset-offsets --to-latest --topic binlog-db40-adData-ad-heat --execute

./bin/kafka-consumer-groups.sh --bootstrap-server kafka-00.ag.alishh:9092 --group es_sync_campaign_record --reset-offsets --to-datetime 2021-01-29T12:00:00.000+0800  --topic binlog-ag-db-41-addata-campaign-record --execute

./bin/kafka-consumer-groups.sh --bootstrap-server kafka-00.ag.alishh:9092 --group dj_ad_campaign --reset-offsets --to-datetime 2021-06-04T11:50:00.000+0800 --all-topics --execute


```
---
# kafka-utils

支持重命名消费组等操作

- [kafka-utils](https://kafka-utils.readthedocs.io/en/latest/index.html)
