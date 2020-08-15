#!/usr/bin/fish
export GITHUB_TOKEN=[REDACTED, but can easily be generated with a Github Account]
cd /mnt/brick/home/dmeier/BuildScour
source venv/bin/activate.fish
python -m BuildScour -l pallets -o builds --log log.txt
python -m BuildScour -l tornadoweb -o builds --log log.txt
python -m BuildScour -l ansible -o builds --log log.txt
zip -r "build_archive_"(date +"%Y%m%dT%H%M")".zip" builds/
