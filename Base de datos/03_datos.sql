INSERT INTO ROLES (nombre_rol, nivel_jerarquia, puede_eliminar_ordenes) VALUES ('Operador', 1, 'N');
INSERT INTO ROLES (nombre_rol, nivel_jerarquia, puede_eliminar_ordenes) VALUES ('Lider', 2, 'S');
INSERT INTO ROLES (nombre_rol, nivel_jerarquia, puede_eliminar_ordenes) VALUES ('Calidad', 2, 'S');
INSERT INTO ROLES (nombre_rol, nivel_jerarquia, puede_eliminar_ordenes) VALUES ('Tecnico', 2, 'S');
INSERT INTO ROLES (nombre_rol, nivel_jerarquia, puede_eliminar_ordenes) VALUES ('Embarques', 2, 'S');
INSERT INTO ROLES (nombre_rol, nivel_jerarquia, puede_eliminar_ordenes) VALUES ('Supervisor', 2, 'S');

INSERT INTO LINEAS_PRODUCCION (codigo_linea, nombre_linea, area) VALUES ('LIN-SMT-01', 'Linea de Ensamble SMT 1', 'Electronica');
INSERT INTO LINEAS_PRODUCCION (codigo_linea, nombre_linea, area) VALUES ('LIN-ENS-02', 'Linea de Ensamble Final 2', 'Arneses');
INSERT INTO LINEAS_PRODUCCION (codigo_linea, nombre_linea, area) VALUES ('LIN-EMP-03', 'Linea de Empaque y Pruebas', 'Embarques');

INSERT INTO CATALOGO_MOTIVOS_PARO (codigo_paro, categoria, descripcion) VALUES ('PAR-01', 'Mantenimiento', 'Falla mecanica o electrica en equipo');
INSERT INTO CATALOGO_MOTIVOS_PARO (codigo_paro, categoria, descripcion) VALUES ('PAR-02', 'Materiales', 'Falta de componente o materia prima');
INSERT INTO CATALOGO_MOTIVOS_PARO (codigo_paro, categoria, descripcion) VALUES ('PAR-03', 'Calidad', 'Defecto detectado en inspeccion');
INSERT INTO CATALOGO_MOTIVOS_PARO (codigo_paro, categoria, descripcion) VALUES ('PAR-04', 'Cambio Modelo', 'Ajuste y preparacion de linea (Set-Up)');
INSERT INTO CATALOGO_MOTIVOS_PARO (codigo_paro, categoria, descripcion) VALUES ('PAR-05', 'Operativo', 'Junta de seguridad o descanso programado');

INSERT INTO EMPLEADOS (num_empleado, nombre_completo, turno, activo, id_rol) VALUES (360258, 'Jair Nagasaki Gavaldon Arrieta', 'MATUTINO', 'S', 6);
INSERT INTO EMPLEADOS (num_empleado, nombre_completo, turno, activo, id_rol) VALUES (374343, 'Erick Guillermo Jaquez Perez', 'MATUTINO', 'S', 2);
INSERT INTO EMPLEADOS (num_empleado, nombre_completo, turno, activo, id_rol) VALUES (111111, 'Benito Juarez', 'NOCTURNO', 'S', 1);
INSERT INTO EMPLEADOS (num_empleado, nombre_completo, turno, activo, id_rol) VALUES (222222, 'Pancho Villa', 'VESPERTINO', 'S', 3);
INSERT INTO EMPLEADOS (num_empleado, nombre_completo, turno, activo, id_rol) VALUES (333333, 'Maria Curie', 'MATUTINO', 'S', 4);
INSERT INTO EMPLEADOS (num_empleado, nombre_completo, turno, activo, id_rol) VALUES (444444, 'Albert Einstein', 'VESPERTINO', 'S', 5);

COMMIT;