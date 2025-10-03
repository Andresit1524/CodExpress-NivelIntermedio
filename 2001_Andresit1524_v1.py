"""
ContactBook (CRUD, POO)
-----------------------
De Andresit1524 (Hayran Andrés López González)

- Clases: Contact y ContactBook.
- Alta/baja/búsqueda case-insensitive (nombre/email) y listado con orden estable apellido,nombre.
- Email duplicado → ERROR:DUP.
- PLUS: persistencia JSON de la lista y un índice por dominio de email @dominio para LIST domain=gmail.com.
- Comandos stdin:
    - `ADD nombre;apellido;email;tel`
    - `DEL email`
    - `FIND texto`
    - `LIST (o LIST domain=...)`. LIST imprime apellido,nombre <email> tel.
- 2001_<ALIAS>_v1.(py|java|cpp)
"""

import json


class Contact:
    """Atributos:
    - nombre
    - apellido
    - email
    - teléfono
    """

    def __init__(self, nombre: str, apellido: str, email: str, tel: int):
        self.nombre = nombre.lower()
        self.apellido = apellido.lower()
        self.email = email.lower()
        self.tel = tel

    # Representación textual del contacto
    def __str__(self):
        return f"{self.nombre} {self.apellido} {self.email} {self.tel}"


class ContactBook:
    def __init__(self):
        # Lista de contactos
        self.contacts = []

    def __str__(self):
        return "\n".join(
            f"{c}: {c.apellido},{c.nombre} <{c.email}> {c.tel}" for c in self.contacts
        )

    def check_emails(self):
        """Verifica si hay emails duplicados en la libreta de contactos

        Para lograrlo, crea un set con los emails y compara la cantidad de elementos.
        Si hay duplicados, el set tendrá menos elementos.
        """

        emails = [c.email for c in self.contacts]
        return len(emails) != len(set(emails))

    def add(self, nombre: str, apellido: str, email: str, tel: int):
        """Añade un contacto a la libreta de contactos.

        - Si el email ya existe, no lo añade y devuelve `ERROR:DUP`.
        - Devuelve `None` si se añade correctamente (por cuestiones de tipado).
        """

        self.contacts.append(Contact(nombre, apellido, email, tel))

        # Verifica si hay emails duplicados tras la adición
        if self.check_emails():
            # Revierte la adición del contacto si es así
            self.contacts.pop()

            return "ERROR:DUP"

        # Ordena los contactos por apellido y luego por nombre
        self.contacts.sort(key=lambda c: (c.apellido, c.nombre))

        # Actualiza la lista de contactos en el archivo JSON
        self.update_json()

        return None

    def del_email(self, email):
        """Elimina un contacto por su email.

        - Si el email no existe, devuelve `ERROR:NOTFOUND`.
        - Devuelve `None` si se elimina correctamente.
        """

        for _, c in enumerate(self.contacts):
            if c.email == email:
                self.contacts.pop()

                return None

        # Actualiza la lista de contactos en el archivo JSON
        self.update_json()

        return "ERROR:NOTFOUND"

    def find(self, texto):
        """Busca contactos que contengan el texto en nombre, apellido o email.

        - La búsqueda es case-insensitive.
        - Devuelve una lista de contactos que coincidan.
        """

        texto = texto
        resultados = [
            f"{c.apellido},{c.nombre}"
            for c in self.contacts
            if texto in c.nombre or texto in c.apellido or texto in c.email
        ]

        return resultados

    def list_contacts(self, domain=None):
        """Lista todos los contactos, o los que coincidan con un dominio específico.

        - Si se proporciona un dominio, filtra los contactos por ese dominio de email.
        - Devuelve una lista de contactos formateados.
        """

        if domain:
            domain = domain.lower()
            resultados = [
                f"{c.apellido},{c.nombre} <{c.email}> {c.tel}\n"
                for c in self.contacts
                if c.email.endswith(f"@{domain}")
            ]
        else:
            resultados = [
                f"{c.apellido},{c.nombre} <{c.email}> {c.tel}\n" for c in self.contacts
            ]

        return resultados

    def update_json(self, filename="contacts.json"):
        """Guarda la lista de contactos en un archivo JSON, sobreescribiéndolo"""

        with open(filename, "w") as f:
            json.dump(
                [
                    {
                        "nombre": c.nombre,
                        "apellido": c.apellido,
                        "email": c.email,
                        "tel": c.tel,
                    }
                    for c in self.contacts
                ],
                f,
            )

# --- TESTS ---
#
# TEST 1: Add and List
# Entrada:
# ADD John;Smith;john.smith@email.com;111222333
# ADD Jane;Doe;jane.doe@email.com;444555666
# LIST
# Salida esperada:
# doe,jane <jane.doe@email.com> 444555666
# smith,john <john.smith@email.com> 111222333
#
# TEST 2: Duplicate and Deletion
# Entrada:
# ADD Peter;Jones;peter.jones@email.com;777888999
# ADD Another;Person;peter.jones@email.com;111222333
# DEL peter.jones@email.com
# LIST
# Salida esperada:
# ERROR:DUP
#
#
# TEST 3: Find (case-insensitive)
# Entrada:
# ADD Mary;Williams;mary.w@email.com;123456789
# ADD David;Brown;david.b@email.com;987654321
# FIND .B@
# Salida esperada:
# brown,david <david.b@email.com> 987654321
#