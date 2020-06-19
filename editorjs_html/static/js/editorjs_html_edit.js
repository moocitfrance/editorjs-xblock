/* Javascript for HtmlXBlock. */
function HtmlXBlockInitEdit(runtime, element, context) {

    $(element).find('.action-cancel').bind('click', function () {
        runtime.notify('cancel', {});
    });

    $(function () {
        var json_data = JSON.parse($('#source_text').text());
        var course_key = 'course'+window.location.pathname.split("+type")[0].split('block')[1];
        var editor = new EditorJS({
          holderId: 'editorjs',
          tools: {
            header: {
              class: Header,
              inlineToolbar: true,
              config: {
                placeholder: 'Header'
              },
              shortcut: 'CMD+SHIFT+H'
            },
            image: {
              class: ImageTool,
              inlineToolbar: true,
              config: {
                endpoints: {
                  // backend file uploader endpoint
                  byFile: window.location.origin+'/editorjs_uploader/'+course_key+'/', 
                }
              }
            },
            list: {
              class: List,
              inlineToolbar: true,
              shortcut: 'CMD+SHIFT+L'
            },
            checklist: {
              class: Checklist,
              inlineToolbar: true,
            },
            quote: {
              class: Quote,
              inlineToolbar: true,
              config: {
                quotePlaceholder: 'Enter a quote',
                captionPlaceholder: 'Quote\'s author',
              },
              shortcut: 'CMD+SHIFT+O'
            },
            warning: Warning,
            marker: {
              class:  Marker,
              inlineToolbar: true,
              shortcut: 'CMD+SHIFT+M'
            },
            code: {
              class:  CodeTool,
              inlineToolbar: true,
              shortcut: 'CMD+SHIFT+C'
            },
            delimiter: Delimiter,
            linkTool: {
              class: LinkTool,
              config: {
                endpoint: window.location.origin+'/editorjs_uploader/'+course_key+'/', 
              }
            },
            embed: Embed,
            table: {
              class: Table,
              inlineToolbar: true,
              shortcut: 'CMD+ALT+T'
            },
            raw: RawTool,
            attaches: {
              class: AttachesTool,
              config: {
                endpoint: window.location.origin+'/editorjs_uploader/'+course_key+'/', 
              }
            },
          },
          data: json_data,
          onChange: function() {
            console.log("onChange");
          }
        });

        $(element).find('.action-save').bind('click', function () {
            editor.save().then((savedData) => {
              var data = {
                  'display_name': $('#html_edit_display_name').val(),
                  'source_text': JSON.stringify(savedData),
              };

              runtime.notify('save', { state: 'start' });

              var handlerUrl = runtime.handlerUrl(element, 'save_html');
              $.post(handlerUrl, JSON.stringify(data)).done(function (response) {
                  if (response.result === 'success') {
                      runtime.notify('save', { state: 'end' });
                  }
                  else {
                      runtime.notify('error', { msg: response.message });
                  }
              });
            });
        });
    });
}
