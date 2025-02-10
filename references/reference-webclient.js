var document;

var gateway = `ws://${window.location.hostname}/ws`;
var websocket;
window.addEventListener('load', onLoad);

function onLoad(event) {
initWebSocket();
}
function initWebSocket() {
  console.log('Trying to open a WebSocket connection...');
  websocket = new WebSocket(gateway);
  websocket.onopen    = onOpen;
  websocket.onclose   = onClose;
  websocket.onmessage = onMessage;
}
function onOpen(event) {
  console.log('Connection opened');
}
function onClose(event) {
  console.log('Connection closed');
  setTimeout(initWebSocket, 2000);
}
function onMessage(event) {
    var dati
    var stringa = event.data;
    if(stringa.startsWith("DT:"))        //aggiorna pagina controllo con i dati ricevuti
    {
       dati = stringa.split("DT:");
       aggiornaStato(dati[1]);
    }
}

// funzioni speciali
function toggleOnOff()
{
    websocket.send('on-off');
}
function toggleCrono()
{
    websocket.send('crono-off-on');
}
function power_up()
{
    websocket.send('power-up');
}
function power_down()
{
    websocket.send('power-dn');
}
function updateSliderTemp(element)
{
    websocket.send('tempSlider'+element);
}

function logoutButton()
{
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/logout", true);
    xhr.send();
    setTimeout(function(){ window.open("./logged-out.html","_self"); }, 500);
}

function sendTimer(element,hour,minute)
{
    if (element.checked)
    {
        server = "/timerSet?ore="+hour+"&min="+minute;
    }
    else
    {
        server = "/timerSet?ore=0"+"&min=0";
    }
    document.getElementById("risposta1").innerHTML = server;
    xhr1 = new XMLHttpRequest();
    xhr1.open("GET", server, true);
    xhr1.send();
}

function aggiornaStato(dati)
{
    //document.getElementById("risposta").innerHTML = dati;
    parametro = dati.split("P");
    for ( i=1 ; i<parametro.length; i++)
    {
        PinPair = parametro[i];
        iparr = PinPair.split("=");
        KEY = iparr[0];
        Valore = iparr[1];
        if (KEY == 0)	//visualizzazione stato TASTO on/off
        {
            if (Valore == 0)
            {
                document.getElementById("switch0").value = 0;
                document.getElementById("image0").src = "OFF.png";
            }
            else
            {
                document.getElementById("switch0").value = 1;
                document.getElementById("image0").src = "ON.png";
            }
        }
        else if (KEY == 1)	//visualizzazione stato cronotermostato
        {
            if (Valore == 1)
            {
                document.getElementById("image3").src = "led-on.png";
            }
            else
            {
                document.getElementById("image3").src = "led-off.png";
            }
        }
        else if (KEY == 2)	//visualizzazione livello potenza
        {
            if (Valore == 0)	//se livello è zero spegni tutto
            {
                document.getElementById("level").src = "LIVELLO-0.png";
            }
            else if (Valore == 1)
            {
                document.getElementById("level").src = "LIVELLO-1.png";
            }
            else if (Valore == 2)
            {
                document.getElementById("level").src = "LIVELLO-2.png";
            }
            else if (Valore == 3)
            {
                document.getElementById("level").src = "LIVELLO-3.png";
            }
            else if (Valore == 4)
            {
                document.getElementById("level").src = "LIVELLO-4.png";
            }
            else if (Valore == 5)
            {
                document.getElementById("level").src = "LIVELLO-5.png";
            }
        }
        else if (KEY == 3)	//visualizzazione setpoint temperatura desiderata
        {
            document.getElementById("tempSlider").value = Valore;		                    //aggiorna posizione slider
            document.getElementById("tempValue").innerHTML = ((Valore-20)/2)+" °C";	//aggiorna valore setpoint impostato
            document.getElementById("tempValueF").innerHTML = ((((Valore-20)/2)*9/5)+32).toFixed(1)+" °F";
        }
        else if (KEY == 4)	//visualizzazione valore sonda 0-255
        {
            document.getElementById("temperature").innerHTML = ((Valore-20)/2).toFixed(1)+" °C";	            //aggiorna valore setpoint impostato
            document.getElementById("temperatureF").innerHTML = ((((Valore-20)/2)*9/5)+32).toFixed(1)+" °F";	//aggiorna valore setpoint impostato
        }
        else if (KEY == 5)	//abilitazione sonda
        {
            if (Valore == 0)//visualizzazione Termoregolazione
            {
                document.getElementById("termoregolazione").style.display = "none";
            }
            else
            {
                document.getElementById("termoregolazione").style.display = "contents";
            }
        }
        else if (KEY == 6)	//abilitazione funzione cronotermostato
        {
            if (Valore == 0)
            {
                document.getElementById("switch2").checked=false;
            }
            else
            {
                document.getElementById("switch2").checked=true;
            }
        }
        else if (KEY == 7)	//visualizzazione stato TIMER on/off
        {
            if (Valore == 0)
            {
                document.getElementById("switch1").checked=false;
            }
            else
            {
                document.getElementById("switch1").checked=true;
            }
        }
        else if (KEY == 8)	//visualizzazione ore timer
        {
            if(document.getElementById("switch1").checked == true)
            {
                if(Valore < 10)
                {
                    Valore = "0"+Valore;
                }
                document.getElementById("ore").innerHTML = Valore+" : ";
            }
            else
            {
                document.getElementById("ore").innerHTML = "- ";
            }
        }
        else if (KEY == 9)	//visualizzazione minuti timer
        {
            if(document.getElementById("switch1").checked == true)
            {
                if(Valore < 10)
                {
                    Valore = "0"+Valore;
                }
                document.getElementById("minuti").innerHTML = Valore+" : ";
            }
            else
            {
                document.getElementById("minuti").innerHTML = "-";
            }
        }
        else if (KEY == 10)	//visualizzazione secondi timer
        {
            if(document.getElementById("switch1").checked == true)
            {
                if(Valore < 10)
                {
                    Valore = "0"+Valore;
                }
                document.getElementById("secondi").innerHTML = Valore;
            }
            else
            {
                document.getElementById("secondi").innerHTML = " -";
            }
        }
        else if (KEY == 11)	//visualizzazione riscaldamento ON/off
        {
            if (Valore == 1)
            {
                document.getElementById("house").src = "CASA-ON.png";
            }
            else
            {
                document.getElementById("house").src = "CASA-OFF.png";
            }
        }
    }
}


we
