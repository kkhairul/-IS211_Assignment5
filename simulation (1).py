#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv
import urllib
import argparse


# In[3]:


def downloadData(url):
    """Opens a URL link.
    
    Args:
        url(str): A string for a website URL.
        
    Returns:
        datafile(various): A variable linked to an applicable datafile found at
        the given URL.
    
    """
    datafile = urllib.urlopen('http://s3.amazonaws.com/cuny-is211-spring2015/requests.csv')
    return datafile


# In[4]:


class Queue:
    """A queue class that stores data."""
    
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)


# In[5]:


class Server(object):
    """A computer server class that performs server functions passed from the simulateOneServer function."""
    
    def __init__(self):
        self.current_task = None
        self.time_remaining = 0

    def tick(self):
        if self.current_task != None:
            self.time_remaining = self.time_remaining - 1
            if self.time_remaining <= 0:
                self.current_task = None

    def busy(self):
        if self.current_task != None:
            return True
        else:
            return False

    def start_next(self, new_task):
        self.current_task = new_task
        self.time_remaining = new_task.get_time()


# In[6]:


class Request(object):
    """A Request class that simulates requests to a server using objects passed from the simulateOneServer function."""
    
    def __init__(self, req_sec, process_time):
        self.timestamp = req_sec
        self.process_time = process_time

    def get_stamp(self):
        return self.timestamp

    def get_time(self):
        return self.process_time

    def wait_time(self, current_time):
        return current_time - self.timestamp


# In[7]:


def simulateOneServer(datafile):
    """Function that simulates a server by operating on a list of requests contained in a file. 
    
    Args:
        datafile(obj): An object pointing to a csv file downloaded from a URL.
        
    Returns:
        str: A string indicating the average wait time, and the size of the
        server queue when it reaches the end of the file.
        
    """
    readfile = csv.reader(datafile)
    lab_server = Server()
    server_queue = Queue()
    waiting_times = []

    for line in readfile:
        req_sec = int(line[0])
        process_time = int(line[2])
        task = Request(req_sec, process_time)
        server_queue.enqueue(task)

        if (not lab_server.busy()) and (not server_queue.is_empty()):
            next_task = server_queue.dequeue()
            waiting_times.append(next_task.wait_time(req_sec))
            lab_server.start_next(next_task)

        lab_server.tick()

    average_wait = sum(waiting_times) / len(waiting_times)
    print('Average Wait %6.2f secs %3d tasks remaining.'
          % (average_wait, server_queue.size()))


# In[8]:


def simulateManyServers(request_file, servers):
    """Function that simulates many servers.
    Args:
        servers_list (list): List of servers to query.
        server_room (dict): Instances of Servers to query.
        
    Returns:
        None
        
    """
    servers_list = [n for n in range(0, int(servers))]
    server_room = {}
    for computer in servers_list:
        server_room[computer] = simulate_one_server
    for data in request_file:
        for serv_num in servers_list:
            random.seed(datetime.datetime.now())
            server_num = random.choice(servers_list)
            server_room[server_num](int(data[0]), int(data[2]))


# In[9]:


def main():
    """Main function downloading, processing, and displaying data."""
    
    if not args.url:
        raise SystemExit
    try:
        datafile = downloadData(args.url)
    except urllib.URLError:
        print ("Please enter a valid URL.")
        raise
    else:
        if not args.servers:
            simulateOneServer(datafile)
        else:
            simulateManyServers(datafile, args.servers)


# In[ ]:




