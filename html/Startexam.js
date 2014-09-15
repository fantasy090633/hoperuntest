function doSubmit() {
	document.form1.action = "scoreAction.do";
	document.form1.submit()
}
var qJson = null, currIndex = 0, curAnswer = -1;
function downloadQuestion() {
	new BaseTool().ajax("downloadQuestion", A, null, false);
	function A(A) {
		qJson = A;
		setQuestion(currIndex)
	}
}
downloadQuestion();
function setQuestion(I) {
	var C = $("qTable");
	for ( var E = C.rows.length; E > 1; E--)
		C.deleteRow(E - 1);
	if (C.rows.length > 1)
		for (E = 0; E < C.rows.length; E++)
			C.deleteRow(1);
	var D = $("qContent");
	D.innerHTML = (currIndex + 1) + "." + qJson[I].QUESTION.CONTENT;
	questionID = qJson[I].QUESTION.QUESTION_ID;
	curAnswer = qJson[I].QUESTION.ANSWER;
	var A = true;
	if (qJson[I].QUESTION.ISCOMPLEX == 1)
		A = false;
	for ( var H = 0; H < qJson[I].OPTIONS.size(); H++) {
		var B = C.insertRow(), G = B.insertCell(), F = B.insertCell();
		if (A)
			G.innerHTML = "<input type=radio name=\"selectitem\" value="
					+ qJson[I].OPTIONS[H].OPTION_ID + ">";
		else
			G.innerHTML = "<input type=checkbox name=\"selectitem\" value="
					+ qJson[I].OPTIONS[H].OPTION_ID + ">";
		F.innerHTML = H + 1 + "." + qJson[I].OPTIONS[H].CONTENT
	}
	currIndex = I + 1
}
function nextQuestion() {
	if (setResult()) {
		if (currIndex == qJson.length - 1) {
			document.form1.nextbutton.style.display = "none";
			document.form1.submitbutton.style.display = ""
		}
		setQuestion(currIndex)
	}
}
function submitResult() {
	doSubmit()
}
function result() {
	if (setResult()) {
		document.form1.action = "verificationAction.do";
		document.form1.submit()
	}
}
function setResult() {
	var B = 0, A = document.getElementsByName("selectitem");
	for ( var D = 0; D < A.length; D++)
		if (A[D].checked)
			B += parseInt(A[D].value);
	if (parseInt(B) <= 0) {
		selectResultWarning();
		return false
	} else {
		var C = "a";
		if (B == curAnswer)
			C = "b";
		document.form1.core.value += (C + ";");
		document.form1.question.value += (questionID + ";");
		return true
	}
}
function setResult1() {
	var B = 0, A = document.getElementsByName("selectitem");
	for ( var D = 0; D < A.length; D++)
		if (A[D].checked)
			B += parseInt(A[D].value);
	var C = "a";
	if (B == curAnswer)
		C = "b";
	document.form1.core.value += (C + ";");
	document.form1.question.value += (questionID + ";");
	return true
}