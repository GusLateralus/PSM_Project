
-- Aquí va la información sobre los médicos registrados
create table usuarios(
usuario_id serial primary key,
nombre_usuario varchar(50) unique not null,
email varchar(100) unique not null,
contrasenia text not null
);

-- Información sobre el paciente
create table pacientes(
paciente_id varchar(18) primary key, -- Esta clave será la CURP del paciente
nombre1 varchar(50) not null,
nombre2 varchar(50),
apellido1 varchar(50) not null,
apellido2 varchar(50),
direccion varchar(110) not null, 
entidad_federativa varchar(50) not null,
usuario_id int,
contacto text not null,
foreign key (usuario_id) references usuarios(usuario_id) on delete cascade
);

-- Aquí se brinda información relacionada a los sensores 
create table sensores(
sensor_id varchar(20) primary key,
nombre_sensor varchar(50),
tipo_sensor varchar(50) not null -- Ponemos este como no nulo para tener una mejor referencia en caso de fallo del sensor
);


-- Tipo de estudio relacionado con la polisomnografía 
create table estudio(
estudio_id serial primary key,
fecha date not null,
hora time not null,
estado varchar(20) not null,
paciente_id varchar(18) not null,
foreign key (paciente_id) references pacientes(paciente_id) on delete cascade
);

-- Aquí irán las mediciones de los sensores:
create table mediciones(
medicion_id serial primary key,
estudio_id serial,
sensor_id varchar(30), 
marca_tiempo timestamp not null, 
valor int not null, 
foreign key (estudio_id) references estudio(estudio_id),
foreign key (sensor_id) references sensores(sensor_id)
);

-- Aquí se darán los resultados del estudio
create table resultados(
resultado_id serial primary key, 
estudio_id serial,
observaciones text,
foreign key (estudio_id) references estudio(estudio_id) on delete cascade
);



-- Datos captados por la cámara
create table camara(
registro_id serial primary key,
marca_tiempo time not null,
tipo_movimiento varchar(50) not null,
detalle_movimiento varchar(50) not null,
estudio_id serial,
foreign key (estudio_id) references estudio(estudio_id) on delete cascade
);
