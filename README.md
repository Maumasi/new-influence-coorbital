
local dev:
use the correct conda env: influance-dev





### build docker-compose
```sh
docker-compose down --remove-orphans && docker-compose up --build
```

### Remove all things docker from disc
[Helpful article](https://jhooq.com/docker-error-no-space-left/)
```sh
docker system prune --all --force

# or

docker image prune -af

# list stored volumes
docker volume ls -qf dangling=true

# remove all volumes
docker volume rm $(docker volume ls -qf dangling=true)
```