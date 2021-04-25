from flask import Flask, request, Markup
from flask import render_template as rt
from subprocess import getoutput

app = Flask("myWeb")

@app.route("/<nav>")
def nav(nav):
    return rt(f"{nav}")

@app.route("/")
def indexpage():
    return rt("index.html")

@app.route("/dockerinfo")
def dockerinfo():
    out = getoutput("docker version")
    output = Markup(f"<pre style='color: white;'>{out}</pre>")
    return output

@app.route("/pullimage", methods=["POST"])
def pullimage():
    if request.method == "POST":
        name = request.form.get("imagename")
        out = getoutput(f"docker pull {name}")
        output = Markup(f"<pre style='color: white;'><center><u>OUTPUT</u></center><br>{out}</pre>")
        return output

@app.route("/deleteimage", methods=["POST"])
def deleteimage():
    if request.method == "POST":
        name = request.form.get("imagename")
        out = getoutput(f"docker rmi {name}")
        output = Markup(f"<pre style='color: white;'><center><u>OUTPUT</u></center><br>{out}</pre>")
        return output

@app.route("/allimages")
def allimages():
    out = getoutput("docker images")
    output = Markup(f"<pre style='color: white;'><center><u>OUTPUT</u></center><br>{out}</pre>")
    return output

@app.route("/launchcontainer", methods=["POST"])
def launchcontainer():
    if request.method == "POST":
        cname = request.form.get("cname")
        iname = request.form.get("imagename")
        out = getoutput(f"docker run -itd --name {cname} {iname}")
        output = Markup(f"<pre style='color: white;'><center><u>OUTPUT</u></center><br>Launched container with id,<br> {out}</pre>")
        return output

@app.route("/startcontainer", methods=["POST"])
def startcontainer():
    if request.method == "POST":
        name = request.form.get("cname")
        out = getoutput(f"docker start {name}")
        output = Markup(f"<pre style='color: white;'><center><u>OUTPUT</u></center><br>container {out} started</pre>")
        return output

@app.route("/stopcontainer", methods=["POST"])
def stopcontainer():
    if request.method == "POST":
        name = request.form.get("cname")
        out = getoutput(f"docker stop {name}")
        output = Markup(f"<pre style='color: white;'><center><u>OUTPUT</u></center><br>container {out} stoped</pre>")
        return output

@app.route("/removecontainer", methods=["POST"])
def removecontainer():
    if request.method == "POST":
        name = request.form.get("cname")
        out = getoutput(f"docker rm -f {name}")
        output = Markup(f"<pre style='color: white;'><center><u>OUTPUT</u></center><br>container {out} removed</pre>")
        return output

@app.route("/allcontainers")
def allcontainers():
    out = getoutput("docker ps -a")
    output = Markup(f"<pre style='color: white;'><center><u>OUTPUT</u></center><br>{out}</pre>")
    return output

@app.route("/installdocker")
def installdocker():
    out = getoutput("ansible-playbook /root/docker/myplaybook/docker.yml")
    output = Markup(f"<pre style='color: white;'><center><u>OUTPUT</u></center><br>{out}</pre>")
    return output

@app.route("/cmd", methods=["POST"])
def cmd():
    if request.method == "POST":
        name = request.form.get("cmd")
        out = getoutput(name)
        output = Markup(f"<pre style='color: white;'><center><u>OUTPUT</u></center><br>{out}</pre>")
        return output

@app.route("/dockerfile", methods=["POST"])
def dockerfile():
    if request.method == "POST":
        layers = request.form.get("layers")
        iname = request.form.get("iname")
        getoutput(f"cat <<EOF > /mydockerfile/Dockerfile \n {layers} \n")
        out = getoutput(f"docker build -t {iname} /mydockerfile")
        output = Markup(f"<pre style='color: white;'><center><u>OUTPUT</u></center><br>{out}</pre>")
        return output

app.run(host="0.0.0.0",port=81)
