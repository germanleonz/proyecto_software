--Agregamos permisos de gestion para User y UserProfile para el grupo de Administradores
INSERT INTO auth_group_permissions (group_id, permission_id) VALUES 
WHERE group_id in (SELECT group_id 
                   FROM auth_group
                   WHERE NAME = "Administradores")
AND permission_id IN (SELECT permission_id
                      FROM auth_permission
                      WHERE NAME = "Can create user")



