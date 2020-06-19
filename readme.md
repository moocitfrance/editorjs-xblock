# editorjs-xblock-html

> Course component (Open edX XBlock) that provides an easy edit HTML component using editorjs: https://editorjs.io/ 


## Copy editorjs_plugin js files
- edx-platform/cms/static/common/js/vendor/editorjs_plugin/

## cms/envs/common.py - register editorjs_plugin files 
```python
base_vendor_js = [
	# load editor js 
	'common/js/vendor/editorjs_plugins/editorjs.js', 
	'common/js/vendor/editorjs_plugins/header.js', 
	'common/js/vendor/editorjs_plugins/image.js', 
	'common/js/vendor/editorjs_plugins/delimiter.js', 
	'common/js/vendor/editorjs_plugins/list.js', 
	'common/js/vendor/editorjs_plugins/checklist.js', 
	'common/js/vendor/editorjs_plugins/quote.js', 
	'common/js/vendor/editorjs_plugins/code.js', 
	'common/js/vendor/editorjs_plugins/embed.js', 
	'common/js/vendor/editorjs_plugins/table.js', 
	'common/js/vendor/editorjs_plugins/link.js', 
	'common/js/vendor/editorjs_plugins/warning.js', 
	'common/js/vendor/editorjs_plugins/marker.js', 
	'common/js/vendor/editorjs_plugins/inline-code.js', 

	# Finally load RequireJS
 	'common/js/vendor/require.js' 
]
```

## lms/envs/common.py - register editorjs_plugin files 
```python
base_vendor_js = [
	# load editor js 
	'common/js/vendor/editorjs_plugins/editorjs.js', 
	'common/js/vendor/editorjs_plugins/header.js', 
	'common/js/vendor/editorjs_plugins/image.js', 
	'common/js/vendor/editorjs_plugins/delimiter.js', 
	'common/js/vendor/editorjs_plugins/list.js', 
	'common/js/vendor/editorjs_plugins/checklist.js', 
	'common/js/vendor/editorjs_plugins/quote.js', 
	'common/js/vendor/editorjs_plugins/code.js', 
	'common/js/vendor/editorjs_plugins/embed.js', 
	'common/js/vendor/editorjs_plugins/table.js', 
	'common/js/vendor/editorjs_plugins/link.js', 
	'common/js/vendor/editorjs_plugins/warning.js', 
	'common/js/vendor/editorjs_plugins/marker.js', 
	'common/js/vendor/editorjs_plugins/inline-code.js', 

	# Finally load RequireJS
 	'common/js/vendor/require.js' 
]
```

## add code for upload images and files to course static assets via editorjs

- Add `editorjs_uploader.py` file into `edx-platform/cms/djangoapps/contentstore/views`
- Register this file into `edx-platform/cms/djangoapps/contentstore/views/__init__.py` by adding this line `from .editorjs_uploader import *`


## Adding new resource into `urlpatterns` inside `common/urls.py`
```python
url(r'^editorjs_uploader/{}/{}?$'.format(settings.COURSE_KEY_PATTERN, settings.ASSET_KEY_PATTERN),
        contentstore.views.editorjs_handler,
        name='editorjs_handler'),
```

## Install xblock
- Using edxapp user and activate virtualenv
- install this plugin using
```shell
pip install -e path-to-editorjs-xblock-html/
```

### Restart your Open edX processes

```shell
sudo /edx/bin/supervisorctl -c /edx/etc/supervisord.conf restart edxapp:
```


## Features

- to do


## Customize the XBlock

We can extend it adding new editorjs plugins.

# Use the XBlock

### Activate the XBlock in your course

Go to `Settings -> Advanced Settings` and add `["editorjs_html"]` in `advanced_modules`.

### Use the XBlock in a unit

Select `Advanced -> EditorJs HTML` in your unit.

## Development environment

For the code quality environment, you need to install both Python and JavaScript requirements.

Run the following:

    npm install -g grunt-cli
    npm install

Then, preferably in a [virtualenv](https://virtualenv.pypa.io), run

    pip install -r requirements.txt


Then, run `grunt test` to assess code quality.

## License

GNU Affero General Public License 3.0 (AGPL 3.0)
