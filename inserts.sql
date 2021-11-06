ALTER TABLE users_user ADD COLUMN rol_id INT;

UPDATE forms_network SET logo='amazon.png' WHERE id=1;
UPDATE forms_network SET logo='amazon-adve.png' WHERE id=2;
UPDATE forms_network SET logo='shopify.png' WHERE id=3;
UPDATE forms_network SET logo='mercado-libre.png' WHERE id=4;

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

UPDATE public.django_site SET  domain='app.crunchdna.com', name='The-Crunch' WHERE id=1;

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

--Insert tipo detalle
INSERT INTO public.endpoint_type_detail(
	id, type)
	VALUES  (1, 'Integer'),
			(2, 'Double' ),
			(3, 'String' ),
			(4, 'Date'   );

--Filtros
INSERT INTO public.filter_filter(
	id, name, detail, type_detail_id, type_filter_id)
	VALUES 	(1, 'Mes Actual', '(cast(FORMAT_DATE("%Y%m", CURRENT_DATE()) AS Integer)*100)', 4, 2),
			(2, 'Año Actual', '(cast(FORMAT_DATE("%Y", CURRENT_DATE()) AS Integer)*10000)', 4, 2),
			(3, 'Fecha Dinamica', NULL, 4, 1);

--Endpoints
INSERT INTO public.endpoint_endpoint(
	id, name_db, name_bc)
	VALUES	(1, 'AuxDimVentasResumen', 'Ventas'),
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
	VALUES (1,'Radiografía','',12,0);

INSERT INTO public.endpoint_access_rol_endpoint (id,description,endpoint_id,rol_id)
	VALUES	(1,'Conexion Ventas',1,0),
			(2,'Conexion Publicidad',3,0),
			(3,'Conexion Inventario',2,0);

INSERT INTO public.charts_user_dashboard (id,edit,"delete",dashboard_id,user_id)
	VALUES (1,0,0,1,12);

INSERT INTO public.charts_row (id,available,column_id,dashboard_id,high_id)
	VALUES	(1,1,4,1,5),
			(2,3,4,1,1),
			(3,0,4,1,1),
			(4,2,4,1,5),
			(5,0,4,1,1);

INSERT INTO public.graphs_graph (id,title,"column",finish,send,endpoint_id,row_id,type_agrupation_id,type_graph_id,xrow_id,type_icon_id,type_time_agrupation_id)
	VALUES	(1,'Total Revenue',1,true,'{"type": "2", "columns": [{"field": "DfSubTotal", "calculate": "sum"}], "dataset": "AuxDimVentasResumen"}',1,1,2,6,NULL,1,NULL),
			(2,'Quantity',1,true,'{"type": "2", "columns": [{"field": "DnQuantityShipped", "calculate": "sum"}], "dataset": "AuxDimVentasResumen"}',1,1,2,6,NULL,1,NULL),
			(3,'Discount',1,true,'{"type": "2", "columns": [{"field": "DfPromotionDiscount", "calculate": "sum"}], "dataset": "AuxDimVentasResumen"}',1,1,2,6,NULL,1,NULL),
			(4,'Tax',1,true,'{"type": "2", "columns": [{"field": "DfTax", "calculate": "sum"}], "dataset": "AuxDimVentasResumen"}',1,1,2,6,NULL,1,NULL),
			(5,'Shipping',1,true,'{"type": "2", "columns": [{"field": "DfShipping", "calculate": "sum"}], "dataset": "AuxDimVentasResumen"}',1,1,2,6,NULL,1,NULL),
			(6,'Ordenes',3,true,'{"type": "2", "columns": [{"field": "DxIdDataFrame"}, {"field": "DxMarketplaceName"}, {"field": "DxOrderId"}, {"field": "DxFulfillmentChannel"}, {"field": "DxOrderStatus"}, {"field": "DnQuantityShipped"}, {"field": "DfPromotionDiscount"}, {"field": "DfShipping"}, {"field": "DfSubTotal"}, {"field": "DnFechaVenta"}], "dataset": "AuxDimVentasResumen"}',1,2,2,5,NULL,NULL,NULL),
			(7,'Inventario',6,true,'{"type": "2", "columns": [{"field": "DxIdDataFrame"}, {"field": "DxMarketplace"}, {"field": "DxAsin"}, {"field": "DxSellerSku"}, {"field": "DxProductName"}, {"field": "DfPriceAmount"}, {"field": "DnTotalQuantity"}], "dataset": "AuxDimInventario"}',2,3,2,5,NULL,NULL,NULL),
			(8,'Impresiones',1,true,'{"type": "2", "columns": [{"field": "DnImpressions", "calculate": "sum"}], "dataset": "AuxDimInventarioAds"}',3,4,2,6,NULL,1,NULL),
			(9,'Clicks',1,true,'{"type": "2", "columns": [{"field": "DnClicks", "calculate": "sum"}], "dataset": "AuxDimInventarioAds"}',3,4,2,6,NULL,1,NULL),
			(10,'Costo',1,true,'{"type": "2", "columns": [{"field": "DfCost", "calculate": "sum"}], "dataset": "AuxDimInventarioAds"}',3,4,2,6,NULL,1,NULL),
			(11,'Ventas Atribuidas',1,true,'{"type": "2", "columns": [{"field": "DfAttributedSales", "calculate": "sum"}], "dataset": "AuxDimInventarioAds"}',3,4,2,6,NULL,1,NULL),
			(12,'PPC',6,true,'{"type": "2", "columns": [{"field": "DxMarketplace"}, {"field": "DxAsin"}, {"field": "DxSellerSku"}, {"field": "DxProductName"}, {"field": "DnImpressions"}, {"field": "DnClicks"}, {"field": "DfCost"}, {"field": "DfAttributedSales"}], "dataset": "AuxDimInventarioAds"}',3,5,2,5,NULL,NULL,NULL);

INSERT INTO public.graphs_graph_filter (id,comparate_value,filter_id,graph_id,value_id,type_comparation_id)
	VALUES	(1,NULL,3,1,12,1),
			(2,NULL,3,2,12,1),
			(3,NULL,3,3,12,1),
			(4,NULL,3,4,12,1),
			(5,NULL,3,5,12,1),
			(6,'(cast(FORMAT_DATE("%Y%m", CURRENT_DATE()) AS Integer)*100)',1,8,31,3),
			(7,'(cast(FORMAT_DATE("%Y%m", CURRENT_DATE()) AS Integer)*100)',1,9,31,3),
			(8,'(cast(FORMAT_DATE("%Y%m", CURRENT_DATE()) AS Integer)*100)',1,10,31,3),
			(9,'(cast(FORMAT_DATE("%Y%m", CURRENT_DATE()) AS Integer)*100)',1,11,31,3);

INSERT INTO public.graphs_yrow (id,"name",graph_id,type_calculate_id,value_id)
	VALUES	(1,'card',1,2,7),
			(2,'card',2,2,8),
			(3,'card',3,2,9),
			(4,'card',4,2,10),
			(5,'card',5,2,11),
			(6,'Plataforma',6,NULL,2),
			(7,'Marketplace',6,NULL,6),
			(8,'# Orden',6,NULL,3),
			(9,'Canal',6,NULL,4),
			(10,'Estado',6,NULL,5),
			(11,'Cantidad',6,NULL,8),
			(12,'Descuento',6,NULL,9),
			(13,'Envio',6,NULL,11),
			(14,'Total',6,NULL,7),
			(15,'Fecha',6,NULL,12),
			(16,'Plataforma',7,NULL,14),
			(17,'Marketplace',7,NULL,15),
			(18,'ASIN',7,NULL,16),
			(19,'SellerSku',7,NULL,17),
			(20,'Nombre',7,NULL,18),
			(21,'Precio',7,NULL,20),
			(22,'Cantidad',7,NULL,19),
			(23,'card',8,2,27),
			(24,'card',9,2,28),
			(25,'card',10,2,29),
			(26,'card',11,2,30),
			(27,'Marketplace',12,NULL,23),
			(28,'ASIN',12,NULL,24),
			(29,'SellerSku',12,NULL,25),
			(30,'Nombre',12,NULL,26),
			(31,'Impresiones',12,NULL,27),
			(32,'Clicks',12,NULL,28),
			(33,'Costo',12,NULL,29),
			(34,'Ventas Atribuidas',12,NULL,30);