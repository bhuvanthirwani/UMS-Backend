from sqlalchemy import Enum


UmsAppsEnum = Enum("app1", "app2", "app3", "app4", "app5", "app6", name="ums_apps")
