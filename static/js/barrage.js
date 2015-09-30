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

$("#send").click(function() {
  var msg = $("#comment").val();
  console.log(msg);
  if (msg) {
    var idName = idNameGen(20);
    var text = '<div id="' + idName + '" class="test-barrage"><a>' + msg + '</a></div>';
    $("#comment-box").append(text)
  }
});
