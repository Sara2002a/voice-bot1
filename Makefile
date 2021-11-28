compose_file := docker/docker-compose.yml
compose := docker-compose -f $(compose_file)

h: help
help:
	@echo -e "\033[1mUSAGE\033[0m"
	@echo "  make COMMAND"
	@echo ""
	@echo "Commands:"
	@echo "  rl, run_local		Running locally for development"
	@echo "  b, build		Build all containers"
	@echo "  u, up, run, install	Build and up containers"
	@echo "  bu, build_and_up	Rebuild and up containers"
	@echo "  rm, remove		Stop and remove containers"
	@echo "  stop			Stop containers"
	@echo "  start			Start containers"
	@echo "  restart		Restart containers"
	@echo "  ps			Show information about running containers"
	@echo "  psa			Show information about all containers"
	@echo "  t, top		Show detailed information about all containers"
	@echo "  sil, show_info_logs	Show logs INFO"
	@echo "  sel, show_error_logs	Show logs ERROR"
	@echo "  sdl, show_docker_logs	Show docker logs"
	@echo "  style			Run black and isort for python code"
	@echo "  h, help		Show help page"

	@echo ""
	@echo -e "\033[1mEXAMPLES\033[0m"
	@echo "  $$ make up"
	@echo "  $$ make build"
	@echo "  $$ make build_and_up"
	@echo ""
	@echo -e "\033[1mNOTE\033[0m: For other container commands use docker or docker-compose."

rl: run_local
run_local:
	poetry run python src/run.py

b: build
build:
	$(compose) build

u: install
up: install
run: install
install:
	$(compose) up -d

bu: build_and_up
build_and_up:
	$(compose) up -d --build

rm: remove
remove:
	$(compose) rm -fs

stop:
	$(compose) stop

start:
	$(compose) start

restart:
	$(compose) restart

ps:
	$(compose) ps

psa:
	$(compose) ps -a

t: top
top:
	$(compose) top

sil: show_info_logs
show_info_logs:
	cat logs/bot_info.log

sel: show_error_logs
show_error_logs:
	cat logs/bot_error.log

sdl: show_docker_logs
show_docker_logs:
	$(compose) logs -f

style:
	black src
	isort src
