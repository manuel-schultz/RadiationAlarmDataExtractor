CREATE TABLE IF NOT EXISTS api_calls (
    id                        INTEGER                                                      NOT NULL PRIMARY KEY AUTOINCREMENT,
    call_action               VARCHAR(128)  DEFAULT NULL,
    call_parameters           VARCHAR(512)  DEFAULT NULL,
    started_at                DATETIME      DEFAULT CURRENT_TIMESTAMP                      NOT NULL,
    ended_at                  DATETIME      DEFAULT CURRENT_TIMESTAMP                      NOT NULL
);

/* Filled by: List of stations / Station information */
CREATE TABLE IF NOT EXISTS stations (
    id                        INTEGER                                                      NOT NULL PRIMARY KEY AUTOINCREMENT,
    api_call_id               INTEGER       DEFAULT 0                                      NOT NULL,
    station_code              VARCHAR(10)   DEFAULT "ATxxxx"                               NOT NULL,
    station_code_country      VARCHAR(2)    DEFAULT "AT"                                   NOT NULL,
    station_code_number       INTEGER       DEFAULT 0                                      NOT NULL,
    german_name               VARCHAR(255)  DEFAULT ""                                     NOT NULL,
    img_coordinates_x         INTEGER       DEFAULT 0                                      NOT NULL,
    img_coordinates_y         INTEGER       DEFAULT 0                                      NOT NULL,
    geo_coordinates_latitude  DECIMAL(11,8) DEFAULT 0.0                                    NOT NULL,
    geo_coordinates_longitude DECIMAL(11,8) DEFAULT 0.0                                    NOT NULL,
    geo_coordinates_elevation DECIMAL(7,2)  DEFAULT 0.0                                    NOT NULL,
    created_at                DATETIME      DEFAULT CURRENT_TIMESTAMP                      NOT NULL,
    updated_at                DATETIME      DEFAULT CURRENT_TIMESTAMP                      NOT NULL,

    CONSTRAINT fk_api_calls FOREIGN KEY (api_call_id) REFERENCES api_calls (id)
);

/* Filled by Station measures */
CREATE TABLE IF NOT EXISTS radiation_levels (
    id                        INTEGER                                                      NOT NULL PRIMARY KEY AUTOINCREMENT,
    uuid                      VARCHAR(36)   DEFAULT "00000000-0000-0000-0000-000000000000" NOT NULL,
    api_call_id               INTEGER       DEFAULT 0                                      NOT NULL,
    station_id                INTEGER       DEFAULT 0                                      NOT NULL,
    measured_at               DATETIME      DEFAULT "1900-01-01 00:00:00"                  NOT NULL,
    measured_timestamp        INTEGER       DEFAULT 0                                      NOT NULL, /* d */
    measured_radiation_value  DECIMAL(6,3)  DEFAULT 0.0, /* v */
    rgb_color                 VARCHAR(16)   DEFAULT "RGB(255,255,255)", /* c */
    hex_color                 VARCHAR(9)    DEFAULT "#FFFFFF",
    created_at                DATETIME      DEFAULT CURRENT_TIMESTAMP                      NOT NULL,
    updated_at                DATETIME      DEFAULT CURRENT_TIMESTAMP                      NOT NULL,

    CONSTRAINT fk_api_calls FOREIGN KEY (api_call_id) REFERENCES api_calls (id)  
    CONSTRAINT fk_stations  FOREIGN KEY (station_id)  REFERENCES stations  (id)  
);

INSERT INTO schema_histories (migration_version) VALUES (1);