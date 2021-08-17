var time =20;
var sec = time*60;
var myTimer = document.getElementById('myTimer');
var myBtn = document.getElementById('myBtn');
window.onload = countDown;

function countDown() {
  var minutes = Math.floor(sec / 60);
  var seconds =sec%60;
    myTimer.innerHTML = (minutes+':'+seconds);



  if (sec <= 0) {
    document.getElementById("myBtn").disabled = true;
      $("#myTimer").fadeTo(2500, 0);
      $("secTimer").fadeTo(2500,0);
    // $("#myBtn").removeAttr("disabled");
    $("#myBtn").removeClass("btnEnable").addClass("btnDisable");

    myBtn.innerHTML = "Timeout!";
    return;
  }
  sec -= 1;
  window.setTimeout(countDown, 1000);
}
