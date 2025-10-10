class Session:
    usuario_actual = None 

    @classmethod
    def iniciar_sesion(cls, usuario):
        cls.usuario_actual = usuario

    @classmethod
    def cerrar_sesion(cls):
        cls.usuario_actual = None

    @classmethod
    def obtener_usuario(cls):
        return cls.usuario_actual
