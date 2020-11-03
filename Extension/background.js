// let changeColor = document.getElementById("changeColor");

// chrome.runtime.onInstalled.addListener(function() {
//   console.log('Works');
// });

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

// (function() {
//     $(document).ready(function() {
//       $('.switch-input').on('change', function() {
//         var isChecked = $(this).is(':checked');
//         var selectedData;
//         var $switchLabel = $('.switch-label');
//         console.log('isChecked: ' + isChecked);

//         if(isChecked) {
//           selectedData = $switchLabel.attr('data-on');
//         } else {
//           selectedData = $switchLabel.attr('data-off');
//         }

//         console.log('Selected data: ' + selectedData);

//       });
//     });

//   })();

// checkbox.addEventListener("change", function () {
//   chrome.storage.sync.get("checkBox", function (items) {
//     alert(items.checkBox);
//   });
// });

// chrome.storage.onChanged.addListener(function(changes, namespace) {
//   for(key in changes) {
//     alert(key == "checkBox")

//   }
// });

// if (jQuery) {
//   alert("loaded")
// } else {
//   alert("not loaded")
// }

chrome.tabs.onUpdated.addListener(function (tabId, changeInfo, tab) {
  var url = tab.url;
  if (url !== undefined && changeInfo.status == "complete") {
    chrome.storage.sync.get(["checkBox"], function (items) {
      // alert(url)
      // if (items.checkBox == "checked") {
      //   $.ajax({
      //     type: "GET",
      //     url: "http://localhost:5000/",
      //     // data: { param: tabURL },
      //     success: callbackFunc,
      //   });
      // }
    });
  }
});

// function callbackFunc(response) {
//   // alert(response);
// }

// chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
//   var tabURL = tabs[0].url;
// alert(tabURL);
// });
// });
