--Rol Default
INSERT INTO public.users_rol(id, rol, duration, "create")
	VALUES	(-1, 'Expirado', 0, 0),
			(0, 'Sin Rol', 0, 0),
			(1, 'Nivel 1', 7, 0),
		    (2, 'Nivel 2', 0, 0),
			(3, 'Nivel 3', 0, 1),
			(4, 'Admin', 0, 1);

--Primer usuario
INSERT INTO public.users_user(
	id, password, is_superuser, username, first_name, last_name, email, is_staff, is_active, rol_id, date_joined, expirate)
	VALUES (-1, 'pbkdf2_sha256$260000$YK80aNZbO9kTUd7xS6USVt$gJUsktOMgzB5Td0AYAtjJnplKodc24RtlF5ohZvMBe0=', true, 'jmateo95', 'Jonathan', 'Mateo', 'joubmaja.69@gmail.com', true, true, 4, current_date, current_date);

INSERT INTO public.account_emailaddress(
	id, email, verified, "primary", user_id)
	VALUES (1, 'joubmaja.69@gmail.com', true, true, -1);

UPDATE public.django_site SET  domain='The-Crunch.com', name='The-Crunch' WHERE id=1;

--Insert tamaños
INSERT INTO public.charts_column(
	id, name, columns, value)
	VALUES 	(1, 'Dos columnas', 2, 6), 
			(2, 'Tres columnas', 3, 4), 
			(3, 'Cuatro columnas', 4, 3),
			(4, 'Seis columnas', 6, 2),
			(5, 'Doce columnas', 12, 1);

INSERT INTO public.charts_high(
	id, name, value)
	VALUES 	(1, 'Muy Grande', 30),
			(2, 'Grande', 25), 
			(3, 'Mediano', 20), 
			(4, 'Pequeño', 15), 
			(5, 'Muy pequeño', 10);

--Insert tipo de iconos
INSERT INTO public.graphs_type_icon(
	id, name, icon, color)
	VALUES 	(1, 'Dollar', 'fe-dollar-sign', 'success'),				
			(2, 'Venta', 'fe-shopping-cart', 'success'),
			(3, 'Quetzal', 'mdi mdi-alpha-q-circle-outline', 'success'),
			(4, 'Numero', 'fe-hash', 'warning'),
			(5, 'Promedio', 'fe-bar-chart-line', 'info '),
			(6, 'Conteo', 'mdi mdi-alpha-c', 'info '),
			(7, 'Sumatoria', 'mdi mdi-plus', 'info ');


--Insert tipo de tiempo de agrupacion
INSERT INTO public.graphs_type_time_agrupation(
	id, name)
	VALUES 	(1, 'Por Mes'),
			(2, 'Por Año'),
			(3, 'Total'	 );

			
--Insert tipo de usuarios
INSERT INTO public.graphs_type_graph(
	id, name, icon)
	VALUES 	(0, 'Espacio Vacio', ''), 
			(1, 'Líneas', 'fas fa-chart-line'), 
			(2, 'Barras Vertical', 'far fa-chart-bar'), 
			(3, 'Barras Horizontal', 'far fa-chart-bar'), 
			(4, 'Pie', 'fas fa-chart-pie'),
			(5, 'Tabla', 'fas fa-table'),
			(6, 'Card', 'fas fa-dice-one');


--Insert tipo Agrupacion
INSERT INTO public.graphs_type_agrupation(
	id, name, card)
	VALUES  (1, 'Leyenda', 'Filas Distintas'),
			(2, 'Columna', 'Todas las Filas' );


--Insert tipo de Calculo
INSERT INTO public.graphs_type_calculate(
	id, name, value)
	VALUES  (1, 'Conteo', 'count'),
			(2, 'Suma', 'sum' ),
			(3, 'Promedio', 'avg' );

--Insert tipo detalle
INSERT INTO public.endpoint_type_detail(
	id, type)
	VALUES  (1, 'Integer'),
			(2, 'Double' ),
			(3, 'String' ),
			(4, 'Date'   );


--Tipo de Filtro
INSERT INTO public.filter_type_filter(
	id, name)
	VALUES	(1, 'Activo'),
			(2, 'Pasivo'),
			(3, 'Estatico');


--Tipo de comparacion
INSERT INTO public.filter_type_comparation(
	id, name, signo)
	VALUES 	(1, 'Mayor que', '>'),
			(2, 'Menor que', '<'),
			(3, 'Mayor o igual que', '>='),
			(4, 'Menor o igual que', '<='),
			(5, 'Igual que', '='),
			(6, 'Diferente de', '!=');

--Filtros
INSERT INTO public.filter_filter(
	id, name, detail, type_detail_id, type_filter_id)
	VALUES 	(1, 'Mes Actual', 'cast(date_trunc(''month'', current_date) as date)', 4, 2),
			(2, 'Año Actual', 'cast(date_trunc(''year'', current_date) as date)', 4, 2),
			(3, 'Fecha Dinamica', NULL, 4, 1);


--Datos de Prueba

--Endpoints
INSERT INTO public.endpoint_endpoint(
	id, name_db, name_bc)
	VALUES (1, 'daily', 'App DMI');

--Endpoint Detail
INSERT INTO public.endpoint_detail(
	id, name_db, name_bc, endpoint_id, type_detail_id)
	VALUES  (1, 'red.keyword', 'Red', 1, 3),
			(2, 'metrics.clicks',  'Clicks',   1, 1),
			(3, 'metrics.impressions',  'Visitas',   1, 1),
			(4, 'date_start', 'Fecha',  1, 4);


--Datos de prueba quenty
--Endpoints
INSERT INTO public.endpoint_endpoint(
	id, name_db, name_bc)
	VALUES (2, 'pickups', 'App Qunety');

--Endpoint Detail
INSERT INTO public.endpoint_detail(
	id, name_db, name_bc, endpoint_id, type_detail_id)
	VALUES  (5, 'id', 'Identificador', 								2, 1),
			(6, 'request_contractor_person_name',  'Presona',   	2, 3),
			(7, 'place_company_name',  'Compañia',   				2, 3),
			(8, 'place_package_location', 'Locacion del paquete',	2, 3),
			(9, 'pickup_physical_weight', 'Peso del paquete',  		2, 2),
			(10, 'created_at', 'Fecha Creación',  					2, 4);

