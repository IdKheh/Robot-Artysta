function ExecPythonCommand(pythonCommand){
    let request = new XMLHttpRequest()
    request.open("GET","/" + pythonCommand, true)
}

//<script src="../static/script.js/"></script>   
    let button1 = document.getElementById("b1").innerHTML;
    let button2 = document.getElementById("b2").innerHTML;
    let button3 = document.getElementById("b3").innerHTML;
    let button4 = document.getElementById("b4").innerHTML;
    console.log("costam");
    button1.addEventListener("mousedown", function()){
    //ExecPythonCommand("action("+id+","1)" )
        console.log("nacisniety");
            
    }
    button1.addEventListener("mouseup",function()){
    //ExecPythonCommand("action("+id+","0)" )
    console.log("puszczony");
    }
