chrome.commands.onCommand.addListener(function (command) {
  if (command === "check_fact") {
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
      const activeTab = tabs[0];
      chrome.scripting.executeScript({
        target: { tabId: activeTab.id },
        function: getSelectedText
      });
    });
  }
});

function getSelectedText() {
  const selectedText = window.getSelection().toString().trim();
  if (selectedText) {
    chrome.runtime.sendMessage({ action: 'factcheck', claim: selectedText });
  } else {
    alert("No text selected!");
  }
}
