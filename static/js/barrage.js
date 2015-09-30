var host = "ws://localhost:8000/chatserver";
var websocket;
$("#close").disabled = true;
$("#connect").click(function() {
  websocket = new WebSocket(host);
  websocket.onopen = function(evt) {};
  websocket.onmessage = function(evt) {
    var newline = '\r\n' + "[" + new Date().toLocaleTimeString() + "]" +
      evt.data;
    $("#chat-box").val($("#chat-box").val() + newline);
    var idName = idNameGen(20);
    var text = '<div id="' + idName + '" class="test-barrage"><a>' + evt.data + '</a></div>';
    $("#comment-box").append(text)


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
  msg = $("#comment").val();
  if (msg) {
    websocket.send(msg);
  }
});

var idNameGen = function(charsLength, chars) {
  var length = charsLength;
  if (!chars)
    var chars = "abcdefghijkmnpqrstuvwxyzABCDEFGHJKMNPQRSTUVWXYZ1234567890";
  var randomChars = "";
  for (x = 0; x < length; x++) {
    var i = Math.floor(Math.random() * chars.length);
    randomChars += chars.charAt(i);
  }
  return 'h' + randomChars;
};
