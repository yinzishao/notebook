
# 基本使用

> https://github.com/taskrabbit/elasticsearch-dump

```bash

docker run --name es-sync --rm -ti elasticdump/elasticsearch-dump \
  --input=http://user:psw@dsn:9200/advertisement_v8.0.0/slogan_data \
  --output=http://user:psw@dsn:9200/slogan_v1.0.0 \
  --type=data --noRefresh --limit=2000 --size=-1 --concurrency=8 \
  --searchBody "{\"query\": {\"range\": {\"updatedAt\": {\"gte\": \"$start\", \"lt\": \"$end\"}}}}"
```


获取父类和子类的同步语句
```
GET advertisement/slogan_data/_search
{
  "query": {
    "has_child": {
      "type": "data",
      "query": {
        "bool": {
          "filter": {
            "range": {
              "createdAt": {
                "gte": "2020-02-24 00:00:00"
              }
            }
          }
        }
      }
    }
  }
}

GET advertisement/data/_search
{
  "query": {
    "bool": {
      "filter": {
        "range": {
          "createdAt": {
            "gte": "2020-02-24 00:00:00"
          }
        }
      }
    }
  }
}
```
---
# 实例

```bash


/home/ymserver/bin/dump_data/node_modules/.bin/elasticdump --type=data --searchBody='{"_source": ["link_hash", "position_list", "material_id", "channel_id", "ocr_image_word_list", "action", "slogan", "city_list", "description", "app_brand_style", "icon", "purpose", "duration", "updatedAt", "app_brand_genre", "materialType", "domain", "resource_list", "platform", "heat", "ad_id", "campaign_id", "screenshot_id", "ocr_video_word_list", "advertiser_id", "tag_list", "totalCount", "campaign_type", "log_summary_list", "media_list", "developer_id", "impression", "createdAt", "format_list", "outer_id", "app_brand_id", "app_brand_industry", "tag_list", "ad_list", "updatedAt", "log_list", "slogan", "ad_cnt", "industry_tag_list", "log_cnt"]}' --input=http://elastic:xxx@dsn:9200/advertisement --output=http://ag_adm:5Oxxx@172.19.42.160:9200/ag_advertisement_copy --size=1200


elasticdump --type=data --searchBody='{"_source": ["ad_list"]}' --input=http://elastic:xxx@dsn:9200/advertisement --output=http://ag_adm:5Oxxx@172.19.42.160:9200/ag_advertisement_copy --size=1200

/home/ymserver/bin/dump_data/node_modules/.bin/elasticdump --type=data --searchBody='{"query": {"bool": {"filter": {"term": {"_id": "a8533654500e7423147188600c27907b"}}}}}' --input=http://elastic:xxx@dsn:9200/advertisement --output=http://ag_adm:5Oxxx@172.19.42.160:9200/advertisement --size=100

/home/ymserver/bin/dump_data/node_modules/.bin/elasticdump --type=data --searchBody='{"query": {"bool": {"filter": {"term": {"_id": "60105383"}}}}}' --input=http://elastic:xxx@dsn:9200/advertisement --output=http://ag_adm:5Oxxx@172.19.42.160:9200/advertisement --size=100


elasticdump --type=data --searchBody='{"_source": ["ad_list"]}' --input=http://ag_adm:5Oxxx@es-test-ag.umlife.net:80/ag_advertisement_v6.5.0/slogan_data --output=$ > ~/tmp/es_ag_advertisement_ec_data.json --size=120

## fileSize参数
elasticdump --type=data --size=2 --fileSize=100mb  --searchBody='{"_source": ["ad_list"]}' --input=http://ag_adm:5Oxxx@es-test-ag.umlife.net:80/ag_advertisement_v6.5.0/slogan_data --output=slogan.json

#得到slogan.json.split-1

##　用了fileSize gzip就没有用了
elasticdump --type=data --size=4 --fileSize=2b  --searchBody='{"_source": ["ad_list"]}' --input=http://ag_adm:5Oxxx@es-test-ag.umlife.net:80/ag_advertisement_v6.5.0/slogan_data --output=$ |gzip > ./1.json.gz

#得到 $.split-3  和空的 1.json.gz


elasticdump --type=data --fileSize=50mb  --searchBody='{"_source": ["ad_list"]}' --input=http://elastic:xxx@dsn:9200/advertisement/slogan_data --output=slogan.json


elasticdump --type=data --searchBody='{"_source": ["_id", "tag_list"], "query": {"bool": {"must": [{"nested": {"path": "tag_list", "query": {"bool": {"filter": {"terms": {"tag_list.tagid": [105, 10501, 10502, 10503, 10504, 10505, 10506, 10507, 10508]}}}}}}], "filter": {"range": {"log_summary_list": {"lt": "2019-09-01 00:00:00", "gte": "2019-08-01 00:00:00"}}}}}}' --input=http://elastic:xxx@dsn:9200/advertisement/data --output=jiaoyu.json --size=1200


elasticdump --type=data  --searchBody='{"_source": ["_id", "tag_list"], "query": {"bool": {"must": [{"nested": {"path": "tag_list", "query": {"bool": {"filter": {"terms": {"tag_list.tagid": [105, 10501, 10502, 10503, 10504, 10505, 10506, 10507, 10508]}}}}}}], "filter": {"range": {"log_summary_list": {"lt": "2019-09-01 00:00:00", "gte": "2019-08-01 00:00:00"}}}}}}'  --input=http://ag_adm:5Oxxx@es-test-ag.umlife.net:80/ag_advertisement_v6.5.0/data --output=slogan.json


/home/ymserver/bin/dump_data/node_modules/.bin/elasticdump --type=data --searchBody='{"query": {"bool": {"filter": {"range": {"createdAt": {"gte": "2019-09-01"}}}}}}' --input=http://elastic:xxx@dsn:9200/advertisement --output=http://ag_adm:5Oxxx@172.19.42.160:9200/ag_advertisement_v7.1.0 --size=1200 --limit=10000

```
