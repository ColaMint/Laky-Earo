/*
Copyright 2016 Everley

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

function earo_ajax(earo_options) {
    options = {
        url: earo_options.url,
        type: earo_options.type,  
        data: earo_options.data,
        dataType: 'json',
        success: function(result) {
            console.log({
                'c': result.c,
                'd': result.d
            });
            if (result.c != 0) {
                toastr.error('{0}({1})'.format(result.d, result.c), 'An error occured');
            } else {
                earo_options.callback(result.d);
            }
        },
        error: typeof(earo_options.error) != undefined ? earo_options.error : function(xhr) {
            toastr.error('{0}({1})'.format(xhr.statusText, xhr.status), 'An error occured');
        },
    } 
    $.ajax(options);
}

function earo_configuration(callback) {
    earo_ajax({
        url: '/configuration',
        callback: callback,
        type: 'GET'
    }); 
}

function earo_source_event_cls_list(callback) {
    earo_ajax({
        url: '/source_event_cls_list',
        callback: callback,
        type: 'GET'
    }); 
}

function earo_processor_list(callback) {
    earo_ajax({
        url: '/processor_list',
        callback: callback,
        type: 'GET'
    }); 
}

function earo_preview_process_flow(source_event_cls_key, callback) {
    earo_ajax({
        url: '/preview_process_flow/' + source_event_cls_key,
        callback: callback,
        type: 'GET'
    }); 
}

function earo_latest_process_flow(source_event_cls_key, callback) {
    earo_ajax({
        url: '/latest_process_flow/' + source_event_cls_key,
        callback: callback,
        type: 'GET'
    }); 
}
