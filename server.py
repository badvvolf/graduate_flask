from flask import Flask, render_template
import subprocess 

app = Flask(__name__)    

no_defense_serv = "192.168.42.142"
active_defense_serv = "192.168.42.153"


@app.route("/")
def hello():
    
    return render_template('index.html')

@app.route("/portscanning")
def portscanning():
    #try nmap

    nmap = subprocess.Popen(["nmap", no_defense_serv, "-p", "20-80"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = nmap.communicate()      
    print output
    nodef_output_lines = output.split("\n")

    nmap = subprocess.Popen(["nmap", active_defense_serv, "-p", "20-80"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = nmap.communicate()      
    print output

    active_def_output_lines = output.split("\n")

    return render_template('portscanning.html', nodefense=nodef_output_lines, actdefense=active_def_output_lines)

@app.route("/dictionary_attack")
def dictionary_attack():
    #try hydra
    argv = ["hydra", "-l", "defender", "-P", "/root/Desktop/passlist.txt", "-t", "4", no_defense_serv, "ssh"]
    hydra = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = hydra.communicate()    
    print output
    print err
    nodef_output_lines = output.split("\n")

    argv = ["hydra", "-l", "defender", "-P", "/root/Desktop/passlist.txt", "-t", "4", active_defense_serv, "ssh"]
    hydra = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = hydra.communicate()    
    print output
    active_def_output_lines = output.split("\n")  

    return render_template('dictionary_attack.html', nodefense=nodef_output_lines, actdefense=active_def_output_lines)




if __name__ == "__main__":              
    app.run(host="0.0.0.0", port=8080)