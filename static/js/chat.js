var host = "ws://localhost:8000/chatserver";
var websocket;
$("#close").disabled = true;
$("#connect").click(function() {
  websocket = new WebSocket(host);
  websocket.onopen = function(evt) {};
  websocket.onmessage = function(evt) {
    var newline = '\r\n' + "[" + new Date().toLocaleTimeString() + "]" +
      evt.data;
    console.log($("#chatbox").val());
    $("#chatbox").val($("#chatbox").val() + newline);


  };
  websocket.onerror = function() {};
  $("#connect").disabled = true;
  $("#close").disabled = false;

  return websocket;
});
$("#close").click(function() {
  websocket.close();
  $("#connect").disabled = false;
  $("#close").disabled = true;
});

$("#send").click(function() {
  msg = $("#to-send").val();
  if (msg) {
    websocket.send(msg);
  }
});
