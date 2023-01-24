(define (domain museum-domain)
  (:requirements :strips)
  (:predicates (at ?x ?y) (adj ?x ?y) (ro ?x))

  (:action move
    :parameters (?a ?from ?to)
    :precondition (and (at ?a ?from)
		       (adj ?from ?to)
           (ro ?a))
    :effect (and (not (at ?a ?from)) (at ?a ?to)))
)
