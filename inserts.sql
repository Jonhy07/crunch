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
			(2, 'Columna', 

--Insert tipo de Calculo
INSERT INTO public.graphs_type_calculate(
	id, name, value)
	VALUES  (1, 'Conteo', 'count'),
			(2, 'Suma', 'sum' ),
			(3, 'Promedio', 'avg' );
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
	VALUES 	(1, 'Mes Actual', '(cast(FORMAT_DATE("%Y%m", CURRENT_DATE()) AS Integer)*100)', 4, 2),
			(2, 'Año Actual', '(cast(FORMAT_DATE("%Y", CURRENT_DATE()) AS Integer)*10000)', 4, 2),
			(3, 'Fecha Dinamica', NULL, 4, 1);

--Insert tipo detalle
INSERT INTO public.endpoint_type_detail(
	id, type)
	VALUES  (1, 'Integer'),
			(2, 'Double' ),
			(3, 'String' ),
			(4, 'Date'   );
--Endpoints
INSERT INTO public.endpoint_endpoint(
	id, name_db, name_bc)
	VALUES (1, 'AuxDimVentasResumen', 'Ventas'),
			(2, 'AuxDimInventario', 'Inventario'),
	 		(3, 'AuxDimInventarioAds', 'Publicidad');

--Endpoint Detail
INSERT INTO public.endpoint_detail(
	id, name_db, name_bc, endpoint_id, type_detail_id)
	VALUES  (1,'DxStoreName',			'Client',				1, 3),
			(2,'DxIdDataFrame',			'Plataform',			1, 3),
			(3,'DxOrderId',				'Order ID',				1, 3),
			(4,'DxFulfillmentChannel',	'Fulfillment Channel',	1, 3),
			(5,'DxOrderStatus',			'Order Status',			1, 3),
			(6,'DxMarketplaceName',		'Marketplace',			1, 3),
			(7,'DfSubTotal',			'Revenue',				1, 2),
			(8,'DnQuantityShipped',		'Quantity',				1, 1),
			(9,'DfPromotionDiscount',	'Discount',				1, 2),
			(10,'DfTax',				'Tax',					1, 2),
			(11,'DfShipping',			'Shipping',				1, 2),
			(12,'DnFechaVenta',			'Date',					1, 4),
			(13,'DxStoreName',			'Client',				2, 3),
			(14,'DxIdDataFrame',		'Plataform',			2, 3),
			(15,'DxMarketplace',		'Marketplace',			2, 3),
			(16,'DxAsin',				'ASIN',					2, 3),
			(17,'DxSellerSku',			'SellerSku',			2, 3),
			(18,'DxProductName',		'Name',					2, 3),
			(19,'DnTotalQuantity',		'Stock',				2, 1),
			(20,'DfPriceAmount',		'Price',				2, 2),
			(21,'DnFechaCarga',			'Date',					2, 4),
			(22,'DxStoreName',			'Client',				3, 3),
			(23,'DxMarketplace',		'Marketplace',			3, 3),
			(24,'DxAsin',				'ASIN',					3, 3),
			(25,'DxSellerSku',			'SellerSku',			3, 3),
			(26,'DxProductName',		'Name',					3, 3),
			(27,'DnImpressions',		'Impresiones',			3, 1),
			(28,'DnClicks',				'Clicks',				3, 1),
			(29,'DfCost',				'Costo',				3, 2),
			(30,'DfAttributedSales',	'Ventas por Publicidad',3, 2),
			(31,'DnFechaCarga',			'Fecha',				3, 4);

INSERT INTO public.charts_dashboard (id,"name",description,user_id,rol_id)
	VALUES (1,'Radiografía','',2,0);

INSERT INTO public.endpoint_access_rol_endpoint (id,description,endpoint_id,rol_id)
	VALUES	(1,'Conexion Ventas',1,0),
			(2,'Conexion Publicidad',2,0),
			(3,'Conexion Inventario',2,0);

INSERT INTO public.charts_user_dashboard (id,edit,"delete",dashboard_id,user_id)
	VALUES (1,1,1,1,13);

INSERT INTO public.charts_row (id,available,column_id,dashboard_id,high_id)
	VALUES	(5,1,4,1,5),
			(6,3,4,1,1),
			(9,0,4,1,1),
			(10,2,4,1,5),
			(11,0,4,1,1);

INSERT INTO public.graphs_graph (id,title,"column",finish,send,endpoint_id,row_id,type_agrupation_id,type_graph_id,xrow_id,type_icon_id,type_time_agrupation_id) 
	VALUES	(9,'Total Revenue',1,true,'{"type": "2", "columns": [{"field": "DfSubTotal", "calculate": "sum"}], "dataset": "AuxDimVentasResumen"}',1,5,2,6,NULL,1,NULL),
			(10,'Quantity',1,true,'{"type": "2", "columns": [{"field": "DnQuantityShipped", "calculate": "sum"}], "dataset": "AuxDimVentasResumen"}',1,5,2,6,NULL,1,NULL),
			(12,'Discount',1,true,'{"type": "2", "columns": [{"field": "DfPromotionDiscount", "calculate": "sum"}], "dataset": "AuxDimVentasResumen"}',1,5,2,6,NULL,1,NULL),
			(13,'Tax',1,true,'{"type": "2", "columns": [{"field": "DfTax", "calculate": "sum"}], "dataset": "AuxDimVentasResumen"}',1,5,2,6,NULL,1,NULL),
			(14,'Shipping',1,true,'{"type": "2", "columns": [{"field": "DfShipping", "calculate": "sum"}], "dataset": "AuxDimVentasResumen"}',1,5,2,6,NULL,1,NULL),
			(19,'Impresiones',1,true,'{"type": "2", "columns": [{"field": "DnImpressions", "calculate": "sum"}], "dataset": "AuxDimInventarioAds"}',3,10,2,6,NULL,1,NULL),
			(16,'Ordenes',3,true,'{"type": "2", "columns": [{"field": "DxOrderId"}, {"field": "DxFulfillmentChannel"}, {"field": "DxMarketplaceName"}, {"field": "DxOrderStatus"}, {"field": "DnQuantityShipped"}, {"field": "DfPromotionDiscount"}, {"field": "DfSubTotal"}, {"field": "DnFechaVenta"}], "dataset": "AuxDimVentasResumen"}',1,6,2,5,NULL,NULL,NULL),
			(20,'Clicks',1,true,'{"type": "2", "columns": [{"field": "DnClicks", "calculate": "sum"}], "dataset": "AuxDimInventarioAds"}',3,10,2,6,NULL,1,NULL),
			(18,'Inventario',6,true,'{"type": "2", "columns": [{"field": "DxAsin"}, {"field": "DxSellerSku"}, {"field": "DxProductName"}, {"field": "DxMarketplace"}, {"field": "DfPriceAmount"}, {"field": "DnTotalQuantity"}], "dataset": "AuxDimInventario"}',2,9,2,5,NULL,NULL,NULL),
			(21,'Costo',1,true,'{"type": "2", "columns": [{"field": "DfCost", "calculate": "sum"}], "dataset": "AuxDimInventarioAds"}',3,10,2,6,NULL,1,NULL),
			(23,'Ventas por Publicidad',1,true,'{"type": "2", "columns": [{"field": "DfAttributedSales", "calculate": "sum"}], "dataset": "AuxDimInventarioAds"}',3,10,2,6,NULL,1,NULL),
			(24,'PPC',6,true,'{"type": "2", "columns": [{"field": "DxMarketplace"}, {"field": "DxAsin"}, {"field": "DxProductName"}, {"field": "DnImpressions"}, {"field": "DnClicks"}, {"field": "DfCost"}, {"field": "DfAttributedSales"}, {"field": "DnFechaCarga"}], "dataset": "AuxDimInventarioAds"}',3,11,2,5,NULL,NULL,NULL);

INSERT INTO public.graphs_graph_filter (id,comparate_value,filter_id,graph_id,value_id,type_comparation_id)
	VALUES	(5,NULL,3,9,12,1),
			(6,NULL,3,10,12,1),
			(8,NULL,3,12,12,1),
			(9,NULL,3,13,12,1),
			(10,NULL,3,14,12,1),
			(11,NULL,3,19,31,1),
			(12,NULL,3,20,31,1),
			(13,NULL,3,21,31,1),
			(14,NULL,3,23,31,1);

INSERT INTO public.graphs_yrow (id,"name",graph_id,type_calculate_id,value_id)
	VALUES	(9,'card',9,2,7),
			(10,'card',10,2,8),
			(12,'card',12,2,9),
			(13,'card',13,2,10),
			(14,'card',14,2,11),
			(16,'# Orden',16,NULL,3),
			(17,'Channel',16,NULL,4),
			(18,'Marketplace',16,NULL,6),
			(19,'Status',16,NULL,5),
			(20,'Quantity',16,NULL,8),
			(21,'Discount',16,NULL,9),
			(22,'Revenue',16,NULL,7),
			(23,'Date',16,NULL,12),
			(28,'ASIN',18,NULL,16),
			(29,'SellerSku',18,NULL,17),
			(30,'Name',18,NULL,18),
			(31,'Marketplace',18,NULL,15),
			(32,'Price',18,NULL,20),
			(33,'Stock',18,NULL,19),
			(34,'card',19,2,27),
			(35,'card',20,2,28),
			(36,'card',21,2,29),
			(37,'card',23,2,30),
			(38,'Marketplace',24,NULL,23),
			(39,'ASIN',24,NULL,24),
			(40,'Name',24,NULL,26),
			(41,'Impresiones',24,NULL,27),
			(42,'Clicks',24,NULL,28),
			(43,'Costo',24,NULL,29),
			(44,'Ventas Atribuidas',24,NULL,30),
			(45,'Fecha',24,NULL,31);