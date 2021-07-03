build:
	docker build -t uchchwhash/podsweeper:latest .

push:
	docker push uchchwhash/podsweeper:latest

apply:
	kubectl apply -f deployment.yaml

delete:
	kubectl delete -f deployment.yaml

list:
	kubectl get pods -n processing

save:
	git commit -a -m meaningless-message
	git push