# Custom admin view
App admin support both custom and default views as defined in `ums.admin.view.create.py` file.


## Keep in mind
- Ensure `__admin__ = False` in your Model class.
- Add new file in `ums.admin.views.custom`
- Add object to `__init__.py` file in the same folder.


## Managing relationships in admin views
- https://stackoverflow.com/questions/33698104/flask-admin-editing-relationship-giving-me-object-representation-of-foreign-key



## References

### Customization options
- https://flask-admin.readthedocs.io/en/latest/introduction/#customizing-built-in-views

### Stack overflow links
- https://stackoverflow.com/questions/13548103/flask-admin-doesnt-show-all-fields
- https://stackoverflow.com/questions/16160507/flask-admin-not-showing-foreignkey-columns
