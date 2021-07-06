build:
	docker build -t mmochan/podsweeper:latest .

push:
	docker push mmochan/podsweeper:latest

apply:
	kubectl apply -f deployment.yaml

delete:
	kubectl delete -f deployment.yaml

list:
	kubectl get pods -n processing

save:
	git commit -a -m meaningless-message
	git push
