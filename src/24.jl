#!/usr/bin/julia

using ProgressBars
using Profile

const OP_MAP = Dict(
    "add" => "+",
    "mul" => "*",
    "div" => "div",
    "mod" => "rem",
    "eql" => "==",
)

function compile(instlist)
    linelist = String[]
    push!(linelist, "function (inputs::AbstractVector{T}) where T <: Integer")

    # push!(linelist, "rev_inputs = Int[]")
    # push!(linelist, "bigend, digit = divrem(n, 10)")
    # push!(linelist, "while bigend > 0")
    # push!(linelist, "append!(rev_inputs, digit)")
    # push!(linelist, "bigend, digit = divrem(bigend, 10)")
    # push!(linelist, "end")
    # push!(linelist, "inputs = reverse(rev_inputs)")

    # push!(linelist, "regs = zeros(T, 4)")
    push!(linelist, "w = 0")
    push!(linelist, "x = 0")
    push!(linelist, "y = 0")
    push!(linelist, "z = 0")
    # push!(linelist, "next = iterate(inputs)")
    push!(linelist, "input_i = 1")
    push!(linelist, "input_max = length(inputs)")
    for inst in instlist
        tokens = split(inst, " ")
        if length(tokens) == 2
            # push!(linelist, "if input_i <= input_max")
            # push!(linelist, "(item, state) = next")
            push!(linelist, "if inputs[input_i] <= 0 || inputs[input_i] > 9")
            push!(linelist, "return 0, 0, 0, 0")
            push!(linelist, "end")
            push!(linelist, "$(tokens[2]) = inputs[input_i]")
            push!(linelist, "input_i += 1")
            # push!(linelist, "next = iterate(inputs, state)")
            # push!(linelist, "end")
        else
            op, a, b = tokens
            opfunc = OP_MAP[op]
            push!(linelist, "$(a) = $(opfunc)($(a), $(b))")
        end
    end
    push!(linelist, "return w, x, y, z")
    push!(linelist, "end")
    expr_str = join(linelist, "\n")
    return Meta.parse(expr_str)
end


function run_func(monad_func, num_iter=9^14)
    works = 0
    digits = repeat([9], 14)
    # for _ in 1:num_iter #ProgressBar(1:num_iter)
    for _ in ProgressBar(1:cld(num_iter, 9^8))
        finished = true
        for _ in 1:9^8
            finished = true
            # @info [reverse(digits)...]
            # @info digits
            w, x, y, z = monad_func(digits)
            # if z == 0
                # @info digits
                # works = sum(d * 10^(14-i) for (i, d) in enumerate(digits))
                # break
            # end
            for di in 14:-1:1
                next_d = digits[di] - 1
                if next_d > 0
                    digits[di] = next_d
                    finished = false
                    break
                end
                digits[di] = 9
            end
            if finished
                break
            end
            # regs = monad_func([digits...])
            # @info regs
        end
        if finished
            break
        end
    end
    return works
end

function make_func()
    lines = open("input/24.txt", "r") do io
        map(strip, readlines(io))
    end
    monad_expr = compile(lines)
    monad_func = eval(monad_expr)
    return monad_expr, monad_func


    # @time count_trees(maze, 1, 3)
    # @timev count_trees(maze, 1, 3)
    # @info "Found answer" count_trees(maze, 1, 3)
    # @timev prod(count_trees(maze, l...) for l in check_list)
    # @info "Found answer" prod(count_trees(maze, l...) for l in check_list)
end

if abspath(PROGRAM_FILE) == @__FILE__
    _, monad_func = make_func()
    @time run_func(monad_func, 10^6)
    # Profile.clear_malloc_data()
    @timev run_func(monad_func, 9^14)
    # Profile.print()
end
