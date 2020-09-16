#!/bin/bash

current_date=2020-09-15
end_date=2020-09-02
while [ "$current_date" != "$end_date" ]; do 
  scrapy crawl innsyn -a start_url="https://holmestrand.kommune.no/innsyn.aspx?response=journalpost_postliste&MId1=307&scripturi=/innsyn.aspx&skin=infolink&fradato=${current_date}T00:00:00"
  current_date=$(date -I -d "$current_date - 1 day")
done