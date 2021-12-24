#!/usr/bin/julia

using ProgressBars

const OP_MAP = Dict(
    "add" => "+",
    "mul" => "*",
    "div" => "div",
    "mod" => "rem",
    "eql" => "==",
)

function compile(instlist)
    linelist = String[]
    push!(linelist, "function monad_func(inputs::AbstractVector{T}) where T <: Integer")

    # push!(linelist, "rev_inputs = Int[]")
    # push!(linelist, "bigend, digit = divrem(n, 10)")
    # push!(linelist, "while bigend > 0")
    # push!(linelist, "append!(rev_inputs, digit)")
    # push!(linelist, "bigend, digit = divrem(bigend, 10)")
    # push!(linelist, "end")
    # push!(linelist, "inputs = reverse(rev_inputs)")

    # push!(linelist, "regs = zeros(T, 4)")
    push!(linelist, "w = zero(T)")
    push!(linelist, "x = zero(T)")
    push!(linelist, "y = zero(T)")
    push!(linelist, "z = zero(T)")
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


function main()
    lines = open("input/24.txt", "r") do io
        map(strip, readlines(io))
    end
    monad_expr = compile(lines)
    eval(monad_expr)
    works = 0
    for digits in ProgressBar(Iterators.product(
        9:-1:1,
        9:-1:1,
        9:-1:1,
        9:-1:1,
        9:-1:1,
        9:-1:1,
        9:-1:1,
        9:-1:1,
        9:-1:1,
        9:-1:1,
        9:-1:1,
        9:-1:1,
        9:-1:1,
        9:-1:1,
    ))
        # @info [reverse(digits)...]
        w, x, y, z = @Base.invokelatest monad_func([reverse(digits)...])
        if z == 0
            @info digits
            works = sum(d * 10^(i-1) for (i, d) in enumerate(digits))
            break
        end
        # regs = monad_func([digits...])
        # @info regs
    end
    @info works
    return monad_expr, monad_func


    # @time count_trees(maze, 1, 3)
    # @timev count_trees(maze, 1, 3)
    # @info "Found answer" count_trees(maze, 1, 3)
    # @timev prod(count_trees(maze, l...) for l in check_list)
    # @info "Found answer" prod(count_trees(maze, l...) for l in check_list)
end

if abspath(PROGRAM_FILE) == @__FILE__
    main()
end
