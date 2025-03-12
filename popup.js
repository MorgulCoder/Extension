document.addEventListener('DOMContentLoaded', function () {
  chrome.storage.local.get(['factcheckResult', 'sources', 'claim'], function (data) {
    const resultDiv = document.getElementById('result');
    const sourcesDiv = document.getElementById('sources');
    const claimDiv = document.getElementById('claimText');

    if (data.claim && data.factcheckResult) {
      claimDiv.textContent = "Claim: " + data.claim;
      resultDiv.textContent = "Result: " + data.factcheckResult;
      
      let sourcesText = "Sources: \n";
      data.sources.forEach(url => {
        sourcesText += url + "\n";
      });
      sourcesDiv.textContent = sourcesText;
    } else {
      resultDiv.textContent = "No fact-checking result available.";
    }
  });
});
