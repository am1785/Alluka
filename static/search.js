// const sanitizer1 = new Sanitizer(); // https://developer.mozilla.org/en-US/docs/Web/API/Element/setHTML

function highlightResult(query) {
// manipulate html output by adding spans and toggling css classes to query text
var texts = document.getElementsByClassName('resultText');  // the div to change
// directly using innerHTML creates a vector for CSS attacks by injecting HTML code, using DOMPurify to sanitize input.
// https://github.com/cure53/DOMPurify
const pattern = /\<(.*?)\>/ig;
query = query.replaceAll(pattern, '\\w+');

Array.from(texts).forEach(element => {
    element.innerHTML = (DOMPurify.sanitize(element.innerHTML.replace(new RegExp('('+ query +')','ig'), '<span class="badge badge-info" >$1</span>')));
});
}

const query = String(document.getElementsByClassName("resultCount")[0].textContent);
var highlightWord = 'NONE';
query !== "No results" ? highlightWord = query.match(new RegExp("\'(.*?)\'", "ig"))[0]: highlightWord = 'NONE';
highlightWord = highlightWord.substring(1, highlightWord.length-1);

if (document.readyState == 'complete') {
    highlightResult(highlightWord);
} else {
    document.onreadystatechange = function () {
        if (document.readyState === "complete") {
            highlightResult(highlightWord);
        }
    }
}
const queryInput = document.getElementById('query');
const noun = document.getElementById('nounBtn');
const pron = document.getElementById('pronBtn');
const adj = document.getElementById('adjBtn');
const verb = document.getElementById('verbBtn');
const adv = document.getElementById('advBtn');
const adp = document.getElementById('adpBtn');
const prt = document.getElementById('prtBtn');
const det = document.getElementById('detBtn');
const conj = document.getElementById('conjBtn');
const num = document.getElementById('numBtn');
const copyAlert = document.getElementById('copy-alert');

function addNoun(){
    queryInput.value += " <" + noun.textContent + "> ";
}
function addPron(){
    queryInput.value += " <" + pron.textContent + "> ";
}
function addAdj(){
    queryInput.value += " <" + adj.textContent + "> ";
}
function addVerb(){
    queryInput.value += " <" + verb.textContent + "> ";
}
function addAdv(){
    queryInput.value += " <" + adv.textContent + "> ";
}
function addAdp(){
    queryInput.value += " <" + adp.textContent + "> ";
}
function addPrt(){
    queryInput.value += " <" + prt.textContent + "> ";
}
function addDet(){
    queryInput.value += " <" + det.textContent + "> ";
}
function addConj(){
    queryInput.value += " <" + conj.textContent + "> ";
}
function addNum(){
    queryInput.value += " <" + num.textContent + "> ";
}

// copy to clipboard implementation

function fallbackCopyTextToClipboard(text) {
    var textArea = document.createElement("textarea");
    textArea.value = text;
    
    // Avoid scrolling to bottom
    textArea.style.top = "0";
    textArea.style.left = "0";
    textArea.style.position = "fixed";
  
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
  
    try {
      var successful = document.execCommand('copy');
      var msg = successful ? 'successful' : 'unsuccessful';
      console.log('Fallback: ' + msg);
    } catch (err) {
      console.error('Fallback: unable to copy', err);
    }
  
    document.body.removeChild(textArea);
  }
  function copyTextToClipboard(text) {
    if (!navigator.clipboard) {
      fallbackCopyTextToClipboard(text);
      return;
    }
    navigator.clipboard.writeText(text).then(function() {
      console.log('Async: Copying was successful!');
    }, function(err) {
      console.error('Async: Could not copy: ', err);
    });
  }

function getCopyContent(element){
    // console.log(element.parentElement.parentElement.parentElement);
    return element.parentElement.parentElement.parentElement.previousElementSibling.children[1].textContent;
}

// implement copy alert auto close fade out

function showAlert() {
    copyAlert.style.visibility = 'visible';
    $("#copy-alert").fadeTo(600, 100).slideUp(200, function() {
      $("#copy-alert").slideUp(500);
    });
  }