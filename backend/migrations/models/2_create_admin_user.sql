-- upgrade --
INSERT INTO users values(1, 'admin', '$2y$10$Ev2JnMs88JMLsOFn5PTOReF4VPUvOfRNuTRAM/mTieFVGcLLV5VIS');
-- downgrade --
DELETE from users where id=1;
