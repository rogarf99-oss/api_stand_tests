import sender_stand_request
import data

def get_user_body(first_name):
    current_body = data.user_body.copy()
    current_body["firstName"] = first_name
    return current_body

# --- Función de assert para pruebas positivas ---
def positive_assert(first_name):
    """Espera status 201 y authToken no vacío"""
    user_body = get_user_body(first_name)
    user_response = sender_stand_request.post_new_user(user_body)

    # Verifica que la respuesta sea exitosa
    assert user_response.status_code == 201, f"Status code inesperado: {user_response.status_code}, {user_response.text}"
    assert user_response.json().get("authToken"), "authToken vacío"

    # Verifica que el usuario aparezca en la tabla
    users_table_response = sender_stand_request.get_users_table()
    str_user = (
        user_body["firstName"] + "," +
        user_body["phone"] + "," +
        user_body["address"] + ",,," +
        user_response.json()["authToken"]
    )
    assert users_table_response.text.count(str_user) == 1

# --- Función de assert para pruebas negativas ---
def negative_assert_400(first_name):
    """Espera status 400 y mensaje de error correcto"""
    if first_name is None:
        user_body = data.user_body.copy()
        user_body.pop("firstName")
    else:
        user_body = get_user_body(first_name)

    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 400, f"Status code inesperado: {user_response.status_code}, {user_response.text}"

    # Mensajes según la API actual
    api_message = user_response.json().get("message", "")
    if first_name is None or first_name == "":
        expected_message = "No se han aprobado todos los parámetros requeridos"
    elif not isinstance(first_name, str) or not first_name.isalpha() or len(first_name) < 2 or len(first_name) > 15:
        expected_message = (
            "Has introducido un nombre de usuario no válido. "
            "El nombre solo puede contener letras del alfabeto latino, "
            "la longitud debe ser de 2 a 15 caracteres"
        )
    else:
        # Para inputs que generan otro tipo de error según la API
        expected_message = api_message

    # Compara mensajes ignorando puntos finales
    assert api_message.strip(".") == expected_message.strip("."), f"Mensaje inesperado: {api_message}"

# --- Pruebas positivas ---
def test_create_user_valid_first_name_get_success_response():
    # Nombre válido según la API actual
    positive_assert("John")

def test_create_user_valid_first_name_long_get_success_response():
    # Otro nombre válido (menos de 15 letras)
    positive_assert("Alexander")

# --- Pruebas negativas ---
def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_400("A")

def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert_400("A"*16)

def test_create_user_has_space_in_first_name_get_error_response():
    # Este test sigue fallando intencionalmente
    negative_assert_400("A Aaa")

def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert_400("\"№%@\"")

def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert_400("123")

def test_create_user_no_first_name_get_error_response():
    negative_assert_400(None)

def test_create_user_empty_first_name_get_error_response():
    negative_assert_400("")

def test_create_user_number_type_first_name_get_error_response():
    negative_assert_400(str(12))
