# FuzzGoat Docker Experiment

```sh
docker build --tag 'fuzzgoat' .
docker run -it -v ./sync_dir/:/src/sync_dir 'fuzzgoat'
```
