-- KEYS: lock keys
-- ARGV[1]: user_id
-- ARGV[2]: ttl (seconds)

local user_id = ARGV[1]
local ttl = tonumber(ARGV[2])

-- Check phase
for i = 1, #KEYS do
    if redis.call("EXISTS", KEYS[i]) == 1 then
        return 0
    end
end

-- Set phase
for i = 1, #KEYS do
    redis.call("SET", KEYS[i], user_id, "EX", ttl)
end

return 1
