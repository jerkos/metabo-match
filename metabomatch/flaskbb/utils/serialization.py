from datetime import datetime


class SerializableMixin:
    def to_json(self):
        d = self.__dict__
        try:
            d.pop('_sa_instance_state')
            d.pop('_password')
        except KeyError:
            pass
        try:
            d['_type'] = self.__tablename__
        except AttributeError:
            pass

        for k, v in d.items():
            try:
                if hasattr(v, '__iter__'):
                    d[k] = [_.to_json() for _ in v]
                else:
                    d[k] = v.to_json()
            except AttributeError:
                try:
                    if isinstance(v, datetime):
                        d[k] = v.isoformat()
                    else:
                        d[k] = v
                except (TypeError, ValueError):
                    d[k] = None
        return d
