# Ever Wonder how our internet find the server from internet? 

We can trace a location of a server using a command line tool called traceroute. Suddenly I thought why not build a simple route visualizer using python dash plotly.

# Prerequisites

*Python3* and *Nodejs* should be installed on your system.

for linux users
```
git clone github.com/muntakim1/route-visualize.git
cd route-visualize
sudo apt install python3-virtualenv gunicorn3
python3 -m venv venv

```



# Requirements

```
pip install -r backend/requirements.txt
```

# Run the python server.

```
gunicon backend.wsgi:serve
```

# For Desktop app (ELECTRONJS)
```
npm i

npm start
```


