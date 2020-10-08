{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Práctica de Introducción al lenguaje Python"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### Ejercicio 1[3 puntos]\n",
    "Se quiere simular una agenda de contactos de forma que de cada contacto se desea almacenar: nombre, apellidos, teléfono, y cuenta de email. \n",
    "El programa debe permitir:\n",
    " 1) Añadir un contacto\n",
    " 2) Eliminar un contacto.\n",
    " 3) Modificar un contacto.\n",
    " 4) Consultar datos de un contacto.\n",
    " 5) Guardar agenda en un fichero.\n",
    " 6) Leer agenda de un fichero\n",
    " 7) Finalizar. Cuando se finaliza,automaticamente guarda la agenda en un fichero de texto."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 44,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Qué quieres hacer? \n",
      "1 para añadir contacto \n",
      "2 para eliminar contacto \n",
      "3 para modificar contacto \n",
      "4 para consultar contacto \n",
      "7 para cerrar el programa \n",
      "1\n",
      "Nombre: \n",
      "ad\n",
      "Apellido 1: \n",
      "ad\n",
      "Apellido 2: \n",
      "ad\n",
      "Telefono: \n",
      "ad\n",
      "Email: \n",
      "ad\n",
      "Contacto ad añadido.\n",
      "\n",
      "Qué quieres hacer? \n",
      "1 para añadir contacto \n",
      "2 para eliminar contacto \n",
      "3 para modificar contacto \n",
      "4 para consultar contacto \n",
      "7 para cerrar el programa \n",
      "2\n",
      "Nombre: \n",
      "ad\n",
      "Contacto ad eliminado.\n",
      "\n",
      "Qué quieres hacer? \n",
      "1 para añadir contacto \n",
      "2 para eliminar contacto \n",
      "3 para modificar contacto \n",
      "4 para consultar contacto \n",
      "7 para cerrar el programa \n",
      "7\n"
     ]
    }
   ],
   "source": [
    "agenda = [];\n",
    "\n",
    "def añadir(nombre, apellido1, apellido2, telefono, email):\n",
    "    contacto = [];\n",
    "    contacto.append(nombre);\n",
    "    contacto.append(apellido1);\n",
    "    contacto.append(apellido2);\n",
    "    contacto.append(telefono);\n",
    "    contacto.append(email);\n",
    "    agenda.append(contacto);\n",
    "    print(\"Contacto \" + nombre + \" añadido.\\n\");\n",
    "    return;\n",
    "\n",
    "def eliminar(nombre):\n",
    "    for i in agenda:\n",
    "        if nombre == i[0]:\n",
    "            agenda.remove(i);\n",
    "            print(\"Contacto \" + nombre + \" eliminado.\\n\");\n",
    "            return;\n",
    "    print(\"No existe pringao.\\n\");\n",
    "    return;\n",
    "\n",
    "def modificar(nombre, newNombre, newApellido1, newApellido2, newTelefono, newEmail):\n",
    "    for i in agenda:\n",
    "        if nombre == i[0]:\n",
    "            i[0] = newNombre;\n",
    "            i[1] = newApellido1;\n",
    "            i[2] = newApellido2;\n",
    "            i[3] = newTelefono;\n",
    "            i[4] = newEmail;\n",
    "            print(\"Contacto \" + newNombre + \" modificado.\\n\");\n",
    "            return;\n",
    "    print(\"No existe pringao.\\n\");\n",
    "    return;\n",
    "\n",
    "def consultar(nombre):\n",
    "    for i in agenda:\n",
    "        if nombre == i[0]:\n",
    "            print(\"Nombre: \" + i[0]);\n",
    "            print(\"Apellido 1: \" + i[1]);\n",
    "            print(\"Apellido 2: \" + i[2]);\n",
    "            print(\"Telefono: \" + i[3]);\n",
    "            print(\"Email: \" + i[4] + \"\\n\");\n",
    "            return;\n",
    "    print(\"No existe pringao.\\n\");\n",
    "    return;\n",
    "\n",
    "entrada = 0;\n",
    "while entrada != \"7\":\n",
    "    entrada = input(\"Qué quieres hacer? \\n\" +\n",
    "                    \"1 para añadir contacto \\n\" +\n",
    "                    \"2 para eliminar contacto \\n\"+\n",
    "                    \"3 para modificar contacto \\n\"+\n",
    "                    \"4 para consultar contacto \\n\"+\n",
    "                    \"7 para cerrar el programa \\n\")\n",
    "    if entrada == \"1\":\n",
    "        nombre = input(\"Nombre: \\n\");\n",
    "        apellido1 = input(\"Apellido 1: \\n\");\n",
    "        apellido2 = input(\"Apellido 2: \\n\");\n",
    "        telefono = input(\"Telefono: \\n\");\n",
    "        email = input(\"Email: \\n\");\n",
    "        añadir(nombre, apellido1, apellido2, telefono, email);\n",
    "    elif entrada == \"2\":\n",
    "        nombre = input(\"Nombre: \\n\");\n",
    "        eliminar(nombre);\n",
    "    elif entrada == \"3\":\n",
    "        nombre = input(\"Nombre: \\n\");\n",
    "        newNombre = input(\"Nuevo nombre: \\n\")\n",
    "        newApellido1 = input(\"Nuevo apellido 1: \\n\");\n",
    "        newApellido2 = input(\"Nuevo Apellido 2: \\n\");\n",
    "        newTelefono = input(\"Nuevo Telefono: \\n\");\n",
    "        newEmail = input(\"Nuevo Email: \\n\");\n",
    "        modificar(nombre, newNombre, newApellido1, newApellido2, newTelefono, newEmail);\n",
    "    elif entrada == \"4\":\n",
    "        nombre = input(\"Nombre: \\n\");\n",
    "        consultar(nombre);"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### Ejercicio 2[4 puntos]\n",
    "Considera el problema de resolver un sistema de 3 ecuaciones por el método de Gauss:\n",
    "https://es.wikipedia.org/wiki/Sistema_de_ecuaciones_lineales#M%C3%A9todo_de_Gauss\n",
    "\n",
    "Se pide implementar un programa que dado un sistema de 3 ecuaciones expresado en forma de una lista de listas donde cada lista representa una ecuación del sistema, devuelva como resultado los valores de las incognitas. \n",
    "\n",
    "Se espera que el sistema que se introduzca tenga solución, pero no hace falta realizar esta comprobación en el código del programa.\n",
    "\n",
    "No se pueden usar ninguna función o método que calcule directamente el determinante."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### Ejercicio 3[3 puntos]\n",
    "El análisis del sentimiento de un texto consiste en asociar al texto un valor numérico que se obtiene de sumar/restar una cantidad por cada aparición de una palabra en el texto de acuerdo a un listado de palabras que tienen valores asociados. Más concretamente si se quiere obtener el análisis del sentimiento, se procesa el texto palabra a palabra:\n",
    "  1) Se toma una palabra, y se busca en la lista de palabras que valor le corresponde.\n",
    "  2) El valor se suma a un contador general.\n",
    "  3) En caso de que la palabra no aparezca, se suma 0.\n",
    "  4) Se pasa a la siguiente palabra\n",
    "  5) Cuando ya no quedan más palabras por procesar del texto, se devuelve el número obtenido.\n",
    "\n",
    "Se pide implementar un programa para calcular el análisis del sentimiento de un texto que será proporcionado a través de un fichero. El listado con las palabras y los valores asociados se proporcionará mediante otro fichero que deberá tener en cada línea del mismo una palabra y un valor separados ambos por un blanco y finalizados por salto de linea. Para realizar el procesamiento no se distinguirá entre mayúsculas y minúsculas. \n",
    "\n",
    "No se pueden usar ninguna función o método que realice directamente el procesamiento."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### Normas de entrega\n",
    "\n",
    "* Fecha tope de entrega: 15/10/2020\n",
    "* La entrega se realizará subiendo al campus virtual un notebook de Jupyter con la solución. El archivo tendrá como nombre IntroPython_GrupoX donde X será el número de grupo correspondiente."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "2"
      ]
     },
     "execution_count": 1,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "1+1"
   ]
  }
 ],
 "metadata": {
  "anaconda-cloud": {},
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 1
}
