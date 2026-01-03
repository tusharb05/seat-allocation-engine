local key = KEYS[1]
local value = ARGV[1]

local curr = redis.call("GET", key)

if not curr then
    return 0
end

if curr == value then
    redis.call("DEL", key)
    return 1
end

return 0
