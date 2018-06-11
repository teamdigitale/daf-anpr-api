prepare:
	curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
	apt -y install git-lfs
	git lfs pull

setup:
	docker-compose up -d elastic kibana
	docker-compose up dataloader

