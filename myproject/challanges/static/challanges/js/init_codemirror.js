document.addEventListener('DOMContentLoaded', function() {
    var textarea = document.querySelectorAll('textarea')[1];
    var editor = CodeMirror.fromTextArea(textarea, {
        mode: 'sql',
        lineNumbers: true,
        theme: 'default'
    });
    editor.setSize('100%', null);
});
