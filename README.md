Importing Data into Slick
=========================

This is a simple utility to help you import data into slick.  It looks at a directory structure,
and syncs the data in it with the slick database.

The directory structure will have files that can be yaml or json.  The attributes for the files are
the same / similar as for the API, however ID's should not be given.  Instead searches will be
performed to make sure everything links up "nicely".

In the structure below a **.json** file can be replaced for any **.yaml** file. Everything
inside the brackets should be replaced.

The following is the directory structure:

    .
    ├── configurations
    │   └── [configuration name].yaml
    └── projects
        └── [project name]
            ├── project.yaml
            ├── components
            │   └── [component name]
            │       ├── component.yaml
            │       └── features
            │           └── [feature name].yaml
            ├── releases
            │   └── [release name]
            │       ├── builds
            │       │   └── [build name].yaml
            │       └── release.yaml
            ├── testcases
            │   └── [testcase name].yaml
            ├── testplans
            │   └── [testplan name].yaml
            └── results
                └── [release name]
                    └── [build name]
                        └── [testrun or testplan name]
                            ├── testrun.yaml
                            └── results
                                └── [testcase name of result]
                                    ├── result.yaml
                                    └── [any other files to attach to result]
    
Install
-------

To install, you'll need python 2.7, virtualenv, and pip.  You should have python development files,
a compiler, and for speed libyaml with it's development files.

simply check out this code and run

    virtualenv virt-python
    virt-python/bin/pip install -r requirements.txt

Usage
-----

There are only a few options to slick-import:

  * **-u or --url**: Specify the url of slick to use.  By default (if you don't specify one) it'll try *http://localhost/slick*.
  * **--delete**: Delete the yaml files after importing.  The default is to leave them.

Also you must specify the directory to import.
