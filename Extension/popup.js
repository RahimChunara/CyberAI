// let changeColor = document.getElementById("changeColor");

// chrome.tabs.onUpdated.addListener(function (tabId, changeInfo, tab) {
//   chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
//     var tabURL = tabs[0].url;
//     console.log(tabURL);
//     $.ajax({
//       type: "POST",
//       url: "/home/rahim/Documents/Github/MajorProject/Extension/script.py",
//       data: { param: tabURL },
//       success: callbackFunc,
//     });
//   });
// });

// function callbackFunc(response) {
//     // do something with the response
//     console.log(response);
// }

// if (jQuery) {  
//   alert("loaded")
// } else {
//   alert("not loaded")
// }

var checkbox = document.querySelector("input[name=myCheck]");

checkbox.addEventListener("change", function () {
  if (this.checked) {
    console.log("checked");
    chrome.storage.sync.set({ checkBox: "checked" }, function () {
      console.log("Settings saved");
    });
  } else {
    console.log("unchecked");
    chrome.storage.sync.set({ checkBox: "unchecked" }, function () {
      console.log("Settings saved");
    });
  }
});



function restoreOptions() {
  // Use default value = false.
  chrome.storage.sync.get(["checkBox"], function (items) {
      // alert(items.checkBox)
      if(items.checkBox == "checked") {
      document.getElementById('checkBox').checked = items.checkBox;
      } else {
      document.getElementById('checkBox').checked = null;
      }
  });
}

document.addEventListener('DOMContentLoaded', restoreOptions);

chrome.tabs.query({ active: true, lastFocusedWindow: true }, (tabs) => {
  let url = tabs[0].url;

  // alert(url);
});
