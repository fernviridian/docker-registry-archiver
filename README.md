# WHAT?

What is this thing? This tool is designed to connect to any docker registry v2 compatible web service and pull all images and image meta data.

# WHY?

Can't you just do a bunch of docker pulls in succession? Yes. But what about that registry that is only served over HTTP? The docker daemon will complain and not pull from it (you can overwrite this behavior so it will pull). What about that image served over TLS/HTTP that has an expired cert? The docker daemon does not like (have not found a way around this). This tool _does not care_ about the docker daemon. It wants to grab all that it can and then leave. 

# REALLY BUT WHY?

I worked with Docker for many months this summer and grew to love it. This is a fun project to learn the Docker V2 Registry API at a HTTP level, and have some fun!
