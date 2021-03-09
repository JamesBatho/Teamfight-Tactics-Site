function allowDrop(ev) {
  ev.preventDefault();
}

function drag(ev) {
  ev.dataTransfer.setData("text", ev.target.id);
}

function drop(ev) {
  ev.preventDefault();
  let data = ev.dataTransfer.getData("text");
  ev.target.appendChild(document.getElementById(data));
}

let composition = [];

let $save = $("#save");
let $name = $("#comp");
let $hexes = $(".hexagon");
$save.on("click", function (e) {
  e.preventDefault();
  getChampData();
});

async function getChampData() {
  const champData = [];
  $hexes.each(function () {
    if (this.children.length > 0) {
      champData.push([this.id, this.children[0].id]);
    }
  });
  if (champData.length !== 8) {
    return;
  }
  console.log(champData);
  let resp = await axios.post("/save", [champData, $name.val()]);
  console.log(resp);
  window.location.href = "http://127.0.0.1:5000/";
}
